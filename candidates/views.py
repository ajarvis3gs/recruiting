from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect
from accounts.models import UserProfile
import xmlrpclib
import base64
from django.conf import settings

from .models import Candidate, CandidateDocument
from .forms import UserApplyStep1Form, UserApplyStep2Form

def view_candidates(request):
    candidates = Candidate.objects.all()

    context = {'candidates': candidates}
    return render(request, 'candidates/candidates.html', context)

def apply(request):

	key = request.GET.get('key', None)
	user = UserProfile.verify_token(key)

	if not key and request.method == 'POST':
		
		form = UserApplyStep1Form(request.POST)

		if form.is_valid():
			data = form.data
			first_name = data['first_name']
			last_name = data['last_name']
			email = data['email']
			citizenship = data['citizenship']
			skype_id = data['skype_id']
			timezone = data['timezone']

			user, created = User.objects.get_or_create(
				first_name=first_name,
				last_name=last_name,
				email=email,
				username=email
				)

			if not created:
				messages.add_message(request, messages.ERROR,
					email + ' has already been registered.')
			else:
				userprofile = UserProfile(
					user=user,
					timezone=timezone,
					citizenship=citizenship,
					skype_id=skype_id,
					user_type='Candidate'
					)

				userprofile.save()
				
				key = user.userprofile.generate_token()
				
				return HttpResponseRedirect(
					reverse('candidate_apply') + '?key=' + key)


	elif not key and request.method == 'GET':
		form = UserApplyStep1Form()

	elif key and user and request.method == 'POST':

		form = UserApplyStep2Form(request.POST, request.FILES)
	
		if form.is_valid():
			files = form.files
			data = form.data
	
			try:
				candidate = user.candidate
				candidate.birth_year = data['birth_year']
				candidate.gender = data['gender']
				candidate.education = data['education']
				candidate.education_major = data['education_major']
				candidate.image = files['image']
				candidate.save()
			except Candidate.DoesNotExist:
				candidate = Candidate.objects.create(user=user, 
					birth_year=data['birth_year'],
					gender=data['gender'],
					education=data['education'],
					education_major=data['education_major'],
					image=files['image']
					)
			CandidateDocument.objects.create(
				candidate=candidate,
				document=files['resume'],
				document_type='Resume'
				)

			messages.add_message(request, messages.SUCCESS,
				'Form submitted successfully.')

			return HttpResponseRedirect(
					reverse('candidate_apply_success') + '?key=' + key)

	elif key and user and request.method == 'GET':
		form = UserApplyStep2Form()

	else:
		messages.add_message(request, messages.ERROR,
			'A valid application key is required to submit documents. ' +
			'Please contact the administrator.')
		form = None

	return render(request, 'candidates/apply.html', {'form': form})


def apply_success(request):
    key = request.GET.get('key', None)
    user = UserProfile.verify_token(key)

    if not key or not user:
        messages.add_message(request, messages.ERROR,
                             'A valid application key is required to view this page.')
    else:
        jobs_url = reverse('jobs') + '?key=' + key
        availability_url = reverse('available', args=[user.id]) + '?key=' + key

    return render(request, 'candidates/apply.html',
                  {'success': 'success',
                   'jobs_url': jobs_url,
                   'availability_url': availability_url
                   })

def pipeline(request, candidate_id):
    candidate = Candidate.objects.get(id=candidate_id)

    # authenticate
    common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(settings.ODOO_SERVER_URL))
    uid = common.authenticate(settings.ODOO_SERVER_DATABASE, settings.ODOO_SERVER_USERNAME, settings.ODOO_SERVER_PASSWORD, {})

    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(settings.ODOO_SERVER_URL))

    for application in candidate.applications.all():
        job = application.job
        hrJobIds = models.execute_kw(settings.ODOO_SERVER_DATABASE, uid, settings.ODOO_SERVER_PASSWORD, 'hr.job', 'search',
                                     [[['name', '=', "%s" % (job.title)]]],
                                     {'limit': 1})

        if hrJobIds:
            # check to see if this candidate exists already
            count = models.execute_kw(settings.ODOO_SERVER_DATABASE, uid, settings.ODOO_SERVER_PASSWORD, 'hr.applicant', 'search_count',
                                      [[['email_from', '=', "%s" % (candidate.email)], ['job_id', '=', hrJobIds[0]]]])

            # create a new candidate
            if count == 0:
                id = models.execute_kw(settings.ODOO_SERVER_DATABASE, uid, settings.ODOO_SERVER_PASSWORD, 'hr.applicant', 'create', [{
                    'partner_name': "%s %s" % (candidate.first_name, candidate.last_name),
                    'display_name': "%s %s" % (candidate.first_name, candidate.last_name),
                    'name': "%s %s" % (candidate.first_name, candidate.last_name),
                    'email_from': '%s' % candidate.email,
                    'partner_phone': '%s' % candidate.phone_number,
                    'job_id': hrJobIds[0]
                }])

                for attachment in candidate.documents.all():
                    file = attachment.document.file
                    file.open(mode='rb')
                    lines = file.read()
                    file.close()

                    id = models.execute_kw(settings.ODOO_SERVER_DATABASE, uid, settings.ODOO_SERVER_PASSWORD, 'ir.attachment', 'create', [{
                        'res_model': 'hr.applicant',
                        'res_id': id,
                        'name': "%s" % attachment.display_name,
                        'display_name': "%s" % attachment.display_name,
                        'datas_fname': "%s" % attachment.display_name,
                        'store_fname': "%s" % attachment.display_name,
                        'type': 'binary',
                        'datas': base64.b64encode(lines)
                    }])

    messages.add_message(request, messages.SUCCESS, 'Candidate pipeline started successfully.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
