from django.contrib import admin

from .models import CandidateDocument, Candidate, CandidateApplication
from interviews.models import InterviewRequest


class InterviewRequestInline(admin.StackedInline):
    model = InterviewRequest
    extra = 1


class CandidateDocumentsInline(admin.StackedInline):
    model = CandidateDocument
    extra = 1


class CandidateAdmin(admin.ModelAdmin):
    def email(obj):
        return ('%s' % (obj.email))

    email.admin_order_field = 'user__email'

    def name(obj):
        return ('%s %s' % (obj.first_name, obj.last_name))

    def applied_to_job(obj):
        if (obj.applications.count() > 0):
            return '%s' % obj.applications.all()[0].job.title
        else:
            return ''

    list_filter = ('initial_contact_date',)
    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'preferred_communication_method', 'best_contact_time', 'initial_contact_date', applied_to_job)
    inlines = (CandidateDocumentsInline, InterviewRequestInline)
    exclude = ('password', 'last_login', 'is_admin',)
    search_fields = ('date_of_birth', 'user__email', 'user__first_name', 'user__last_name',)


class CandidateApplicationAdmin(admin.ModelAdmin):
    list_filter = ('created',)
    search_fields = ('created',)


admin.site.register(Candidate, CandidateAdmin)
admin.site.register(CandidateApplication, CandidateApplicationAdmin)
