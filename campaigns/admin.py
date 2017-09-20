from django.contrib import admin
from .models import MessageTemplate, MailCampaign

class MailCampaignAdmin(admin.ModelAdmin):
    def start_campaign_link(self):
        return "<a href='/campaigns/mailcampaign/%s/start'>start campaign</a>" % self.id

    start_campaign_link.allow_tags = True
    list_display = ('name', 'job', 'message_template', 'is_active', start_campaign_link)

class MessageTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')


admin.site.register(MailCampaign, MailCampaignAdmin)
admin.site.register(MessageTemplate, MessageTemplateAdmin)

