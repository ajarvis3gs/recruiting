from django.contrib import admin

from .models import Employer, EmployerContact, EmployerDocument, EmployerPricingSchedule


class EmployerContactsInline(admin.StackedInline):
    model = EmployerContact
    can_delete = True
    verbose_name_plural = 'Employer Contacts'


class EmployerDocumentsInline(admin.StackedInline):
    model = EmployerDocument
    can_delete = True
    verbose_name_plural = 'Employer Documents'


class EmployerAdmin(admin.ModelAdmin):
    inlines = (EmployerContactsInline, EmployerDocumentsInline,)
    exclude = ('password', 'last_login', 'is_staff')
    list_display = ('name', 'code', 'address', 'phone_number', 'is_active')

class EmployerPricingScheduleAdmin(admin.ModelAdmin):
    list_display = ('employer', 'region', 'service_group', 'job_title', 'experience_level', 'demand', 'hourly_wage', 'hourly_rate', 'is_active')
    list_filter = ('region', 'service_group', 'job_title', 'experience_level', 'demand',)
    # list_editable = ('region', 'service_group', 'job_title', 'experience_level', 'demand', 'hourly_rate', 'hourly_wage', 'is_active')

class EmployerContactAdmin(admin.ModelAdmin):
    def user_full_name(self, obj):
        return obj.user.get_full_name()

    user_full_name.short_description = 'Name'

    def user_email(self, obj):
        return obj.user.email

    user_email.short_description = 'Email'

    def user_phone_number(self, obj):
        return obj.user.userprofile.phone_number

    exclude = ('password', 'last_login', 'is_staff')
    list_display = ('user_full_name', 'user_email', 'user_phone_number', 'is_active')

admin.site.register(Employer, EmployerAdmin)
admin.site.register(EmployerContact, EmployerContactAdmin)
admin.site.register(EmployerPricingSchedule, EmployerPricingScheduleAdmin)
