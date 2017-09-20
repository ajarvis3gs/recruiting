from django.contrib import admin

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
    inlines = (JobMandatoryQualificationsInline, JobRequestedQualificationsInline, JobAdditionalInformationRequestsInline, JobDocumentsInline, )
    list_display = ('employer', 'title', 'employer_contact', 'agency', 'submission_date', 'target_rate', 'vendor_rate')
    list_filter = ('employer', 'agency', 'submission_date')
    search_fields = ('title', 'agency')

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