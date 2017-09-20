from __future__ import unicode_literals

from django.db import models
from jobs.models import Job
from vendors.models import VendorContact
from recruiting.choices import *

class MessageTemplate(models.Model):
    name = models.CharField(max_length=100)
    subject = models.CharField(blank=True, null=True, max_length=100)
    body = models.TextField(null=True, blank=True,)
    is_active = models.BooleanField(default=True)
    last_modified = models.DateTimeField(auto_now_add=False, auto_now=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return "%s" % (self.name)

class MailCampaign(models.Model):
    name = models.CharField(max_length=100)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='campaigns', null=True, blank=True)
    message_template = models.ForeignKey(MessageTemplate, on_delete=models.CASCADE, related_name='campaigns')
    vendor_contacts = models.ManyToManyField(VendorContact, blank=True)
    is_active = models.BooleanField(default=True)
    last_modified = models.DateTimeField(auto_now_add=False, auto_now=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return "%s" % (self.name)