""" recruiting URL Configuration """
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from recruiting import signals
from interviews import views as interviewsViews
from jobs import views as jobsViews
from publicsite import views as publicViews
from candidates import views as candidatesViews
from recruiters import views as recruitersViews
from dashboards import views as dashboardViews
from campaigns import views as campaignViews

urlpatterns = [
    url(r'^$', publicViews.home, name='home'),
    url(r'^home/$', publicViews.home, name='home'),
    url(r'^services/$', publicViews.services, name='services'),
    url(r'^portfolio/$', publicViews.portfolio, name='portfolio'),
    url(r'^about/$', publicViews.about, name='about'),
    url(r'^careers/$', publicViews.careers, name='careers'),
    url(r'^careers/(?P<job_id>\d+)/$', publicViews.career_details, name='career_details'),
    url(r'^careers/(?P<job_id>\d+)/apply/$', publicViews.career_apply, name='career_apply'),
    url(r'^dashboards/$', dashboardViews.dashboards, name='dashboards'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^jobs/$', jobsViews.view_jobs, name='jobs'),
    url(r'^jobs/xml_feed$', jobsViews.xml_feed, name='xml_feed'),
    url(r'^jobs/(?P<job_id>\d+)/$', jobsViews.view_job_details, name='job_details'),
    url(r'^jobs/(?P<job_id>\d+)/apply/$', jobsViews.apply, name='apply'),
    url(r'^jobs/(?P<job_id>\d+)/unpublish/$', jobsViews.unpublish, name='unpublish'),
    url(r'^jobs/(?P<job_id>\d+)/publish/$', jobsViews.publish, name='publish'),
    url(r'^jobs/fetch/$', jobsViews.fetch, name='fetch'),
    url(r'^campaigns/mailcampaign/(?P<campaign_id>\d+)/start/$', campaignViews.start_campaign, name='start_campaign'),
    url(r'^candidates/apply/$', candidatesViews.apply, name='candidate_apply'),
    url(r'^candidates/apply/success/$', candidatesViews.apply_success, name='candidate_apply_success'),
    url(r'^recruiters/', recruitersViews.view_recruiters, name='recruiters'),
    url(r'^available/(?P<bu_id>\d+)/$', interviewsViews.available, name='available'),
    url(r'^availability/(?P<bu_id>\d+)/$', interviewsViews.availability, name='availability'),
    url(r'^interviews/', interviewsViews.interview_requests, name='interviews'),
]