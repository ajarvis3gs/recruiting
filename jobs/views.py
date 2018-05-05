from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import render
from models import Job
from candidates.models import Candidate, CandidateDocument
from interviews.models import InterviewRequest
from accounts.models import UserProfile
from django_mailbox.models import Mailbox
from django.shortcuts import redirect
from django.template.loader import get_template
from django.template import Context
import datetime as dt
from datetime import date, datetime
from candidates.forms import ApplyNowForm
from django.contrib.auth.models import User


""" PUBLIC SITE VIEWS """


def home(request):
    context = {}
    return render(request, 'jobs/home.html', context)


def services(request):
    context = {}
    return render(request, 'jobs/services.html', context)


def portfolio(request):
    context = {}
    return render(request, 'jobs/portfolio.html', context)


def about(request):
    context = {}
    return render(request, 'jobs/about.html', context)


def careers(request):
    jobs = Job.objects.filter(is_active__exact=True).filter(submission_date__gte=date.today()).order_by('-created')
    context = {'jobs': jobs}
    return render(request, 'jobs/careers.html', context)


def career_details(request, job_id):
    job = Job.objects.get(id=job_id)
    context = {'job': job}
    return render(request, 'jobs/career_details.html', context)


def career_apply(request, job_id):
    job = Job.objects.get(id=job_id)

    # make sure this is a post
    if request.method == 'POST':
        # create the new document
        form = ApplyNowForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                user = User.objects.create_user(form.cleaned_data['firstName'], 'job%s-%s' % (job.id, form.cleaned_data['email']), 'changeme')
                user.first_name = form.cleaned_data['firstName']
                user.last_name = form.cleaned_data['lastName']
                user.save()

                userProfile = UserProfile()
                userProfile.user = user
                userProfile.phone_number = form.cleaned_data['phone']
                userProfile.save()

                candidate = Candidate()
                candidate.user = user
                candidate.save()

                interviewRequest = InterviewRequest()
                interviewRequest.candidate = candidate
                interviewRequest.job = job
                interviewRequest.save()

                doc = CandidateDocument(document=request.FILES['resume'])
                doc.display_name = form.cleaned_data['resume']
                doc.candidate = candidate
                doc.save()
            except:
                return render(request, 'jobs/career_apply.html', {'job': job, 'status': 'error'})

        return render(request, 'jobs/career_apply.html', {'job': job, 'status': 'success'})
    else:
        return render(request, 'jobs/career_apply.html', {'job': job, 'status': 'new'})


""" SECURE SITE VIEWS """


def add_interview_requests(request, user, jobs_ids):
    try:
        candidate = user.candidate
    except Candidate.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'This user is not a candidate.')
        return
    except:
        raise

    for job_id in jobs_ids:
        ir = InterviewRequest(candidate=candidate, job=Job.objects.get(pk=int(job_id)))
        ir.save()

    if 'requested_jobs' in request.session:
        del request.session['requested_jobs']

    messages.add_message(request, messages.SUCCESS, 'Form submitted successfully.')


def view_jobs(request):
    key = request.GET.get('key', None)
    user = UserProfile.verify_token(key)

    if request.method == 'GET':
        jobs = Job.objects.all().order_by('-created')
        context = {'jobs': jobs}

    if request.method == 'POST':
        jobs_ids = request.POST.getlist('requested_jobs[]')

        if request.user.is_anonymous() and (not key or not user):
            request.session['add_new_jobs_pending'] = True
            request.session['requested_jobs'] = jobs_ids
            request.session['redirect_to'] = reverse('jobs')
            return HttpResponseRedirect(reverse('account_login'))

        context = {}

        if not user:
            user = request.user

        add_interview_requests(request, user, jobs_ids)

    return render(request, 'jobs/jobs.html', context)


def view_job_details(request, job_id):
    job = Job.objects.get(id=job_id)
    context = {'job': job}
    return render(request, 'jobs/details.html', context)


def fetch(request):
    mailboxes = Mailbox.active_mailboxes.all()

    msg_count = 0
    for mailbox in mailboxes:
        print 'Gathering messages for %s' % mailbox.name
        msgs = mailbox.get_new_mail()
        msg_count = msg_count + len(msgs)
        for message in msgs:
           print 'Received %s (from %s)' % (message.subject, message.from_address)

    messages.add_message(request, messages.SUCCESS, '%s jobs fetched from email' % msg_count)

    return redirect('/')


# XML job feed.  Used by indeed.
def xml_feed(request):
    jobs = Job.objects.filter(is_active__exact=True).filter(is_featured__exact=True).filter(submission_date__gte=date.today()).order_by('-id')
    context = {'jobs': jobs}

    template = get_template('jobs/xml_feed.html')
    context = Context(context)
    xml = template.render(context)

    return HttpResponse(xml, content_type='text/xml')


def apply(request, job_id):
    job = Job.objects.get(id=job_id)
    context = {'job': job}
    return render(request, 'jobs/apply.html', context)


def unpublish(request, job_id):
    job = Job.objects.get(id=job_id)

    job.is_featured = False
    job.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def publish(request, job_id):
    job = Job.objects.get(id=job_id)

    job.is_featured = True
    job.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))