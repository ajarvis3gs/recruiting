from django.contrib import admin

from .models import Vendor, VendorContact, VendorDocument

class VendorContactsInline(admin.StackedInline):
    model = VendorContact
    can_delete = True
    verbose_name_plural = 'Vendor Contacts'

class VendorDocumentsInline(admin.StackedInline):
    model = VendorDocument
    can_delete = True
    verbose_name_plural = 'Vendor Documents'

class VendorAdmin(admin.ModelAdmin):
    inlines = (VendorContactsInline, VendorDocumentsInline, )
    exclude = ('password', 'last_login', 'is_staff')
    list_display = ('name', 'code', 'address', 'phone_number', 'is_active')

class VendorContactAdmin(admin.ModelAdmin):
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

admin.site.register(Vendor, VendorAdmin)
admin.site.register(VendorContact, VendorContactAdmin)