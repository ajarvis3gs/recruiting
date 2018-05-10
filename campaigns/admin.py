from django.contrib import admin
from .models import MessageTemplate, MailCampaign

class MailCampaignAdmin(admin.ModelAdmin):
    def start_campaign_link(self):
        if self.vendor_contacts.count() > 0:
            return "<a href='/campaigns/mailcampaign/%s/startVendor'>email vendors</a>" % self.id
        elif self.candidates.count() > 0:
            return "<a href='/campaigns/mailcampaign/%s/startCandidate'>email candidates</a>" % self.id
        else:
            return "select recipients"

    def vendor_contact_count(self):
        return self.vendor_contacts.count()

    def submission_date(self):
        return self.job.submission_date

    def vendor_submission_date(self):
        return self.job.vendor_submission_date

    start_campaign_link.allow_tags = True
    list_display = ('name', 'job', 'message_template', submission_date, vendor_submission_date, 'is_active', start_campaign_link)

class MessageTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')


admin.site.register(MailCampaign, MailCampaignAdmin)
admin.site.register(MessageTemplate, MessageTemplateAdmin)

