from django.contrib import admin
from datetime import date, datetime

from .models import Job, JobAdditionalInformationRequest, JobMandatoryQualification, JobRequestedQualification, JobDocument

class JobMandatoryQualificationsInline(admin.StackedInline):
    model = JobMandatoryQualification
    can_delete = False
    verbose_name_plural = 'Job Mandatory Qualifications'


class JobRequestedQualificationsInline(admin.StackedInline):
    model = JobRequestedQualification
    can_delete = False
    verbose_name_plural = 'Job Requested Qualifications'


class JobAdditionalInformationRequestsInline(admin.StackedInline):
    model = JobAdditionalInformationRequest
    can_delete = False
    verbose_name_plural = 'Job Additional Information Requests'


class JobDocumentsInline(admin.StackedInline):
    model = JobDocument
    can_delete = True
    verbose_name_plural = 'Job Documents'


class JobAdmin(admin.ModelAdmin):
    def job_actions(self):
        if self.is_featured:
            return "<a href='/jobs/%s/unpublish'>unpublish</a>" % self.id
        else:
            return "<a href='/jobs/%s/publish'>publish</a>" % self.id

    def is_open(self):
        if self.submission_date >= date.today():
            return u'<img src="/static/admin/img/icon-yes.svg" alt="True">'
        else:
            return u'<img src="/static/admin/img/icon-no.svg" alt="False">'

    inlines = (JobMandatoryQualificationsInline, JobRequestedQualificationsInline, JobAdditionalInformationRequestsInline, JobDocumentsInline, )
    list_display = ('id', 'employer', 'title', 'employer_contact', 'agency', 'submission_date', 'target_rate', 'vendor_rate', is_open, job_actions)
    list_filter = ('employer', 'agency', 'submission_date', 'is_featured')
    search_fields = ('title', 'agency', 'preferred_software')
    job_actions.allow_tags = True
    is_open.allow_tags = True


class JobDocumentAdmin(admin.ModelAdmin):
    def download_link(self):
        if self.document:
            return "<a href='%s' download='%s'>download</a>" % (self.document.url, self.display_name)
        else:
            return "No document"

    download_link.allow_tags = True

    list_display = ('job', 'display_name', 'file_type', download_link)
    verbose_name_plural = 'Job Documents'


admin.site.register(Job, JobAdmin)
admin.site.register(JobDocument, JobDocumentAdmin)