from django.contrib import admin

from .models import CandidateDocument, Candidate, CandidateApplication, CandidateResponse, CandidateResponseMandatoryQualification, CandidateResponseRequestedQualification
from interviews.models import InterviewRequest

class CandidateResponseMandatoryQualificationInline(admin.TabularInline):
    model = CandidateResponseMandatoryQualification
    extra = 1


class CandidateResponseRequestedQualificationInline(admin.TabularInline):
    model = CandidateResponseRequestedQualification
    extra = 1


class InterviewRequestInline(admin.TabularInline):
    model = InterviewRequest
    extra = 1


class CandidateDocumentsInline(admin.TabularInline):
    model = CandidateDocument
    extra = 1


class CandidateAdmin(admin.ModelAdmin):
    def odoo(self):
        return "<a href='/candidates/%s/odoo'>odoo</a>" % self.id

    def email(obj):
        return ('%s' % (obj.email))

    email.admin_order_field = 'user__email'

    def name(obj):
        return ('%s %s' % (obj.first_name, obj.last_name))

    def applied_to_job(obj):
        if (obj.applications.count() > 0):
            return "<a href='/admin/jobs/job/%s/change'>%s: %s</a>" % (obj.applications.all()[0].job.id, obj.applications.all()[0].job.id, obj.applications.all()[0].job.title)
        else:
            return ''

    def resume(obj):
        if obj.documents.count() > 0:
            return "<a href='%s' download='%s'>download resume</a>" % (obj.documents.all()[0].document.url, obj.documents.all()[0].display_name)
        else:
            return ""

    applied_to_job.allow_tags = True
    resume.allow_tags = True
    odoo.allow_tags = True


    list_filter = ('status',)
    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'preferred_communication_method', 'best_contact_time', 'status', applied_to_job, resume, odoo)
    inlines = (CandidateDocumentsInline, InterviewRequestInline)
    exclude = ('password', 'last_login', 'is_admin',)
    search_fields = ('email', 'first_name', 'last_name', 'phone_number')


class CandidateApplicationAdmin(admin.ModelAdmin):
    list_filter = ('created',)
    search_fields = ('created',)


class CandidateResponseAdmin(admin.ModelAdmin):
    list_filter = ('created',)
    search_fields = ('created',)
    inlines = (CandidateResponseMandatoryQualificationInline, CandidateResponseRequestedQualificationInline)


admin.site.register(Candidate, CandidateAdmin)
admin.site.register(CandidateApplication, CandidateApplicationAdmin)
admin.site.register(CandidateResponse, CandidateResponseAdmin)
