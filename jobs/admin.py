from django.contrib import admin
from datetime import date, datetime

from .models import Job, JobAdditionalInformationRequest, JobMandatoryQualification, JobRequestedQualification, JobDocument

class JobMandatoryQualificationsInline(admin.TabularInline):
    model = JobMandatoryQualification
    can_delete = False
    verbose_name_plural = 'Job Mandatory Qualifications'
    extra = 1


class JobRequestedQualificationsInline(admin.TabularInline):
    model = JobRequestedQualification
    can_delete = False
    verbose_name_plural = 'Job Requested Qualifications'
    extra = 1


class JobAdditionalInformationRequestsInline(admin.TabularInline):
    model = JobAdditionalInformationRequest
    can_delete = False
    verbose_name_plural = 'Job Additional Information Requests'
    extra = 1


class JobDocumentsInline(admin.TabularInline):
    model = JobDocument
    can_delete = True
    verbose_name_plural = 'Job Documents'
    extra = 1


class JobAdmin(admin.ModelAdmin):
    def publish(self):
        if self.is_featured:
            return "<a href='/jobs/%s/unpublish'>unpublish</a>" % self.id
        else:
            return "<a href='/jobs/%s/publish'>publish</a>" % self.id

    def is_open(self):
        if self.submission_date >= date.today():
            return u'<img src="/static/admin/img/icon-yes.svg" alt="True">'
        else:
            return u'<img src="/static/admin/img/icon-no.svg" alt="False">'

    def apps(self):
        return self.applications.count()

    inlines = (JobMandatoryQualificationsInline, JobRequestedQualificationsInline, JobAdditionalInformationRequestsInline, JobDocumentsInline, )
    list_display = ('id', 'employer', 'title', 'employer_contact', 'agency', 'submission_date', 'target_rate', 'vendor_rate', is_open, apps, publish)
    list_filter = ('employer', 'agency', 'submission_date', 'is_featured')
    search_fields = ('title', 'agency', 'preferred_software')
    publish.allow_tags = True
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