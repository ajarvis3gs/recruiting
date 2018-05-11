from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from datetime import date, datetime
from candidates.models import Candidate
from jobs.models import Job

from interviews.models import InterviewInvitation, InterviewRequest
from jobs.models import Job

@login_required
def dashboards(request):
    if request.user.is_authenticated:

        user_type = request.user.userprofile.user_type

        if user_type == 'Candidate':
            return render(request, 'candidates/dashboard.html')

        if user_type == 'Recruiter':
            initial_contacts_sent = Candidate.objects.filter(initial_contact_date__isnull=True).count()
            response_forms_sent = Candidate.objects.filter(response_form_sent_date__isnull=False).count()
            response_forms_completed = Candidate.objects.filter(response_form_completed_date__isnull=False).count()
            open_jobs = Job.objects.filter(is_active__exact=True).filter(is_featured__exact=True).filter(submission_date__gte=date.today()).count()

            context = {
                'initial_contacts_sent': initial_contacts_sent,
                'response_forms_sent': response_forms_sent,
                'response_forms_completed': response_forms_completed,
                'open_jobs': open_jobs,
            }

            return render(request, 'recruiters/dashboard.html', context)

        if user_type == 'Employer':
            return render(request, 'employers/dashboard.html')

    return render(request, 'dashbaords/home.html')