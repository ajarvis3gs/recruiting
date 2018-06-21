from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import render
from models import Job
from employers.models import Employer
from candidates.models import Candidate
from interviews.models import InterviewRequest
from accounts.models import UserProfile
from django_mailbox.models import Mailbox
from django.shortcuts import redirect
from django.template.loader import get_template
from django.template import Context
import datetime as dt
from django.db.models import Q
from datetime import date, datetime
from django.contrib.sites.models import Site
from publicsite.models import SiteDetail, SiteArticle


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
    site = Site.objects.get_current()
    siteDetail = SiteDetail.objects.get(site=site)

    employer3gs = Employer.objects.get(code='3GS')

    jobs = Job.objects.filter(is_active__exact=True).filter(is_featured__exact=True).filter(submission_date__gte=date.today())

    if site.name == '1x3i':
        jobs.exclude(employer_id__exact=employer3gs.id)

    jobs.order_by('-id')
    context = {'jobs': jobs, 'site': site, 'siteDetail': siteDetail}

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