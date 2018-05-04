""" recruiting URL Configuration """
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from interviews import views as interviewsViews
from jobs import views as jobsViews
from candidates import views as candidatesViews
from recruiters import views as recruitersViews
from dashboards import views as dashboardViews
from campaigns import views as campaignViews

urlpatterns = [
    url(r'^$', jobsViews.home, name='home'),
    url(r'^services/$', jobsViews.services, name='services'),
    url(r'^portfolio/$', jobsViews.portfolio, name='portfolio'),
    url(r'^about/$', jobsViews.about, name='about'),
    url(r'^careers/$', jobsViews.careers, name='careers'),
    url(r'^careers/(?P<job_id>\d+)/$', jobsViews.career_details, name='career_details'),
    url(r'^careers/(?P<job_id>\d+)/apply/$', jobsViews.career_apply, name='career_apply'),
    url(r'^dashboards/$', dashboardViews.dashboards, name='dashboards'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^jobs/$', jobsViews.view_jobs, name='jobs'),
    url(r'^jobs/xml_feed$', jobsViews.xml_feed, name='xml_feed'),
    url(r'^jobs/(?P<job_id>\d+)/$', jobsViews.view_job_details, name='job_details'),
    url(r'^jobs/(?P<job_id>\d+)/apply/$', jobsViews.apply, name='apply'),
    url(r'^jobs/fetch/$', jobsViews.fetch, name='fetch'),
    url(r'^campaigns/mailcampaign/(?P<campaign_id>\d+)/start/$', campaignViews.start_campaign, name='start_campaign'),
    url(r'^candidates/apply/$', candidatesViews.apply, name='candidate_apply'),
    url(r'^candidates/apply/success/$', candidatesViews.apply_success, name='candidate_apply_success'),
    url(r'^recruiters/', recruitersViews.view_recruiters, name='recruiters'),
    url(r'^available/(?P<bu_id>\d+)/$', interviewsViews.available, name='available'),
    url(r'^availability/(?P<bu_id>\d+)/$', interviewsViews.availability, name='availability'),
    url(r'^interviews/', interviewsViews.interview_requests, name='interviews'),
]