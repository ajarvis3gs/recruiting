from django.contrib import admin

from .models import InterviewRequest, InterviewInvitation, Availability

class InterviewRequestAdmin(admin.ModelAdmin):
    def job_listing(self):
        return "%s: %s" % (self.job.id, self.job.title)

    list_display = ('candidate', 'candidate_accepted', job_listing, 'employer_accepted')
    search_fields = ('candidate__user__username', 'candidate__user__email',
        'candidate__user__first_name', 'candidate__user__last_name',
        'job__employer__user__username', 'job__employer__user__email',
        'job__employer__user__first_name', 'job__employer__user__last_name',
        'job__employer__name',)

admin.site.register(InterviewRequest, InterviewRequestAdmin)

class InterviewInvitationAdmin(admin.ModelAdmin):
    search_fields = ('uuid', 'candidate__user__username', 'candidate__user__email',
        'candidate__user__first_name', 'candidate__user__last_name',
        'job__employer__user__username', 'job__employer__user__email',
        'job__employer__user__first_name', 'job__employer__user__last_name',
        'job__employer__name',)
    list_display = ('candidate', 'job', 'status', 'confirmed_time', 'uuid')
    list_filter = ('status', 'confirmed_time',)

admin.site.register(InterviewInvitation , InterviewInvitationAdmin)

class AvailabilityAdmin(admin.ModelAdmin):
    pass

admin.site.register(Availability, AvailabilityAdmin)
