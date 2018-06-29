from django.shortcuts import render
from jobs.models import Job
from candidates.models import Candidate, CandidateDocument, CandidateApplication, CandidateResponse, CandidateResponseRequestedQualification, CandidateResponseMandatoryQualification
from interviews.models import InterviewRequest
from accounts.models import UserProfile
from datetime import date, datetime
from candidates.forms import ApplyNowForm
from forms import ContactUsForm
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from models import SiteDetail, SiteArticle
from django.core.mail import send_mail
from django.contrib.auth.models import User
import cgi
from django.shortcuts import redirect
from django_mailbox.models import MessageAttachment
from campaigns.views import initial_contact_campaign, candidate_campaign, response_form_campaign
import xmlrpclib
import base64
from django.conf import settings

def home(request):
    site = Site.objects.get_current()
    siteDetail = SiteDetail.objects.get(site=site)
    context = {'site': site, 'siteDetail': siteDetail}
    if request.method == 'POST':
        form = ContactUsForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                send_mail(
                    'New Contact Us Request',
                    'Name: %s, Email: %s, Comment: %s' % (
                        form.cleaned_data['name'],
                        form.cleaned_data['email'],
                        form.cleaned_data['comments']
                    ),
                    siteDetail.info_email,
                    [siteDetail.info_email],
                    fail_silently=True
                )
            except:
                return render(request, 'home.html', context)

    return render(request, 'home.html', context)


def services(request):
    site = Site.objects.get_current()
    siteDetail = SiteDetail.objects.get(site=site)

    context = {'site': site, 'siteDetail': siteDetail}
    return render(request, 'services.html', context)


def portfolio(request):
    site = Site.objects.get_current()
    siteDetail = SiteDetail.objects.get(site=site)

    context = {'site': site, 'siteDetail': siteDetail}
    return render(request, 'portfolio.html', context)


def about(request):
    site = Site.objects.get_current()
    siteDetail = SiteDetail.objects.get(site=site)

    context = {'site': site, 'siteDetail': siteDetail}
    return render(request, 'about.html', context)


def careers(request):
    site = Site.objects.get_current()
    siteDetail = SiteDetail.objects.get(site=site)
    jobs = Job.objects.filter(is_active__exact=True).filter(submission_date__gte=date.today()).order_by('-created')

    context = {'jobs': jobs, 'site': site, 'siteDetail': siteDetail}
    return render(request, 'careers.html', context)


def career_details(request, job_id):
    site = Site.objects.get_current()
    siteDetail = SiteDetail.objects.get(site=site)
    try:
        job = Job.objects.get(id=job_id)
        context = {'job': job, 'site': site, 'siteDetail': siteDetail}
    except:
        return redirect('careers')

    return render(request, 'career_details.html', context)


def career_response_form(request, job_id, candidate_id):
    site = Site.objects.get_current()
    siteDetail = SiteDetail.objects.get(site=site)
    try:
        job = Job.objects.get(id=job_id)
        candidate = Candidate.objects.get(id=candidate_id)
    except:
        return redirect('careers')

    if request.method == 'POST':
        step = request.POST['step']
        if step == '1':
            candidate.first_name = request.POST['firstName']
            candidate.last_name = request.POST['lastName']
            candidate.email = request.POST['email']
            candidate.phone_number = request.POST['phone']
            candidate.work_status = request.POST['workStatus']
            candidate.referral_method = request.POST['referralMethod']
            candidate.save()

            candidateResponse = CandidateResponse()
            candidateResponse.job = job
            candidateResponse.candidate = candidate
            candidateResponse.save()

            return render(request, 'career_response_form.html', {'response': candidateResponse, 'job': job, 'candidate': candidate, 'status': 'step2', 'site': site, 'siteDetail': siteDetail})
        if step == '2':
            candidateResponse = CandidateResponse.objects.get(id=request.POST['responseId'])
            # loop over each mandatory qualification
            for qualification in job.mandatoryQualifications.all():
                if ('mandatoryQualification_%s_response' % qualification.id) in request.POST:
                    qualificationResponse = CandidateResponseMandatoryQualification()
                    qualificationResponse.candidateResponse = candidateResponse
                    qualificationResponse.mandatoryQualification = qualification
                    qualificationResponse.responseText = request.POST['mandatoryQualification_%s_response' % qualification.id]
                    qualificationResponse.save()

            # save responses

            return render(request, 'career_response_form.html', {'response': candidateResponse, 'job': job, 'candidate': candidate, 'status': 'step3', 'site': site, 'siteDetail': siteDetail})
        if step == '3':
            candidateResponse = CandidateResponse.objects.get(id=request.POST['responseId'])

            # loop over each requested qualification
            for qualification in job.requestedQualifications.all():
                if ('requestedQualification_%s_response' % qualification.id) in request.POST:
                    qualificationResponse = CandidateResponseRequestedQualification()
                    qualificationResponse.candidateResponse = candidateResponse
                    qualificationResponse.requestedQualification = qualification
                    qualificationResponse.responseText = request.POST['requestedQualification_%s_response' % qualification.id]
                    qualificationResponse.save()

            # save responses
            candidate.response_form_completed_date = datetime.now()
            candidate.status='Response Form Completed'
            candidate.save()

            send_mail(
                '%s %s has completed the candidate response form for job %s - %s' % (candidate.first_name, candidate.last_name, job.id, cgi.escape(job.title)),
                'Please login to the portal for details',
                siteDetail.support_email,
                [siteDetail.support_email],
                fail_silently=True
            )

            return render(request, 'career_response_form.html', {'response': candidateResponse, 'job': job, 'candidate': candidate, 'status': 'success', 'site': site, 'siteDetail': siteDetail})

    return render(request, 'career_response_form.html', {'job': job, 'candidate': candidate, 'status': 'step1', 'site': site, 'siteDetail': siteDetail})


def career_apply(request, job_id):
    site = Site.objects.get_current()
    siteDetail = SiteDetail.objects.get(site=site)
    try:
        job = Job.objects.get(id=job_id)
    except:
        return redirect('careers')

    # make sure this is a post
    if request.method == 'POST':
        # create the new document
        form = ApplyNowForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                candidate = Candidate()
                candidate.first_name = form.cleaned_data['firstName']
                candidate.last_name = form.cleaned_data['lastName']
                candidate.email = form.cleaned_data['email']
                candidate.preferred_communication_method = form.cleaned_data['preferredCommunicationMethod']
                candidate.best_contact_time = form.cleaned_data['bestContactTime']
                candidate.phone_number = form.cleaned_data['phone']
                candidate.status='New'
                candidate.save()

                candidateApplication = CandidateApplication()
                candidateApplication.candidate = candidate
                candidateApplication.job = job
                candidateApplication.save()

                if request.FILES.get('resume', False):
                    doc = CandidateDocument(document=request.FILES['resume'])
                    doc.display_name = form.cleaned_data['resume']
                    doc.candidate = candidate
                    doc.save()

                # create the initial contact campaign
                campaign = initial_contact_campaign(job, candidate)
                candidate_campaign(site, siteDetail, campaign)

                # create the response form campaign but don't start it just yet
                response_form_campaign(job, candidate)

                # send to our crm system
                sendToOdoo(candidate.id, job)
            except Exception as e:
                print(e)
                send_mail(
                    'Error submitting application for job %s - %s' % (job.id, cgi.escape(job.title)),
                    'Error submitting an application from %s %s (%s). %s' % (
                        form.cleaned_data['firstName'],
                        form.cleaned_data['lastName'],
                        form.cleaned_data['email'],
                        e.message),
                    siteDetail.support_email,
                    [siteDetail.support_email],
                    fail_silently=True
                )
                return render(request, 'career_apply.html', {'job': job, 'status': 'error', 'site': site, 'siteDetail': siteDetail, 'errorMessage': e.message})

        return render(request, 'career_apply.html', {'job': job, 'status': 'success', 'site': site, 'siteDetail': siteDetail})
    else:
        return render(request, 'career_apply.html', {'job': job, 'status': 'new', 'site': site, 'siteDetail': siteDetail})


def sendToOdoo(candidate_id, job):
    candidate = Candidate.objects.get(id=candidate_id)

    # authenticate
    common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(settings.ODOO_SERVER_URL))
    uid = common.authenticate(settings.ODOO_SERVER_DATABASE, settings.ODOO_SERVER_USERNAME, settings.ODOO_SERVER_PASSWORD, {})

    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(settings.ODOO_SERVER_URL))

    hrJobIds = models.execute_kw(settings.ODOO_SERVER_DATABASE, uid, settings.ODOO_SERVER_PASSWORD, 'hr.job', 'search',
                            [[['name', '=', "%s" % (job.title)]]],
                            {'limit': 1})

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
