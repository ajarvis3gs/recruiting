from django.contrib import admin

from .models import CandidateDocument, Candidate
from interviews.models import InterviewRequest


class InterviewRequestInline(admin.StackedInline):
    model = InterviewRequest


class CandidateDocumentsInline(admin.StackedInline):
    model = CandidateDocument


class CandidateAdmin(admin.ModelAdmin):
    def email(obj):
        return ('%s' % (obj.user.email))

    email.admin_order_field = 'user__email'

    def name(obj):
        return ('%s' % (obj.user.get_full_name()))

    def user_phone_number(obj):
        return obj.user.userprofile.phone_number

    list_filter = ('gender',)
    list_display = (name, email, user_phone_number)
    inlines = (CandidateDocumentsInline, InterviewRequestInline)
    exclude = ('password', 'last_login', 'is_admin',)
    search_fields = ('date_of_birth', 'user__email', 'user__first_name', 'user__last_name',)


admin.site.register(Candidate, CandidateAdmin)
