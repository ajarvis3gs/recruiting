from django.shortcuts import render
from jobs.models import Job
from candidates.models import Candidate, CandidateDocument
from interviews.models import InterviewRequest
from accounts.models import UserProfile
from datetime import date, datetime
from candidates.forms import ApplyNowForm
from forms import ContactUsForm
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from models import SiteDetail, SiteArticle
from django.core.mail import send_mail

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
    job = Job.objects.get(id=job_id)

    context = {'job': job, 'site': site, 'siteDetail': siteDetail}
    return render(request, 'career_details.html', context)


def career_apply(request, job_id):
    site = Site.objects.get_current()
    siteDetail = SiteDetail.objects.get(site=site)
    job = Job.objects.get(id=job_id)

    # make sure this is a post
    if request.method == 'POST':
        # create the new document
        form = ApplyNowForm(request.POST, request.FILES)
        if form.is_valid():
            #try:
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

            if request.FILES.get('resume', False):
                doc = CandidateDocument(document=request.FILES['resume'])
                doc.display_name = form.cleaned_data['resume']
                doc.candidate = candidate
                doc.save()

            send_mail(
                'New Job Application for job %s - %s' % (job.id, job.title),
                'A new application was submitted for job %s - %s.  Please login to the portal to view the application detail.' % (
                    job.id,
                    job.title
                ),
                siteDetail.jobs_email,
                [siteDetail.jobs_email],
                fail_silently=True
            )
            #except:
            #    return render(request, 'career_apply.html', {'job': job, 'status': 'error', 'site': site, 'siteDetail': siteDetail})

        return render(request, 'career_apply.html', {'job': job, 'status': 'success', 'site': site, 'siteDetail': siteDetail})
    else:
        return render(request, 'career_apply.html', {'job': job, 'status': 'new', 'site': site, 'siteDetail': siteDetail})
