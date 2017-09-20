from django.contrib import admin

from .models import Recruiter

class RecruiterAdmin(admin.ModelAdmin):
    def user_full_name(self, obj):
        return obj.user.get_full_name()

    user_full_name.short_description = 'Name'

    def user_email(self, obj):
        return obj.user.email

    user_email.short_description = 'Email'

    def user_phone_number(self, obj):
        return obj.user.userprofile.phone_number

    list_display = ('user_full_name', 'user_email', 'user_phone_number', 'is_active')
    exclude = ('password', 'last_login', 'is_staff', 'thumb')

admin.site.register(Recruiter, RecruiterAdmin)