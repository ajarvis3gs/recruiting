from django.shortcuts import render
from campaigns.models import MailCampaign
import logging, os
from django.contrib import messages
from django.http import HttpResponse
from django.template import Template, Context
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.conf import settings
from django.http import HttpResponseRedirect

logger = logging.getLogger(__name__)

def start_campaign(request, campaign_id):
    # load the campaign
    mailCampaign = MailCampaign.objects.get(id=campaign_id)

    messageBody = merge_template(mailCampaign.message_template.body, mailCampaign.job)
    messageSubject = merge_template(mailCampaign.message_template.subject, mailCampaign.job)

    # send to contacts
    emailAddresses = []

    # accumulate vendor contact email addresses (if existing)
    for vendorContact in mailCampaign.vendor_contacts.all():
        emailAddresses.append(vendorContact.user.email)

    # accumulate candidate email addresses (if existing)
    for candidate in mailCampaign.candidates.all():
        emailAddresses.append(candidate.user.email)

    email = EmailMultiAlternatives(
        messageSubject,
        messageBody,
        settings.DEFAULT_FROM_EMAIL,
        None,
        emailAddresses
    )

    for document in mailCampaign.job.documents.all():
        content = open(document.document.path, 'rb').read()
        email.attach(document.display_name, content)

    email.send()

    messages.add_message(request, messages.SUCCESS, '%s emails delivered successfully.' % len(emailAddresses))

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def merge_template(template, job):
    # create the dataset
    data = {}
    data['job'] = job

    template = Template(template)
    context = Context(data)
    return template.render(context)