from django.shortcuts import render
from campaigns.models import MailCampaign
import logging
from django.http import HttpResponse
from django.template import Template, Context
from django.core.mail import EmailMessage, EmailMultiAlternatives

logger = logging.getLogger(__name__)

def start_campaign(request, campaign_id):
    # load the campaign
    mailCampaign = MailCampaign.objects.get(id=campaign_id)

    print "found campaign id %s" % mailCampaign

    messageBody = merge_template(mailCampaign.message_template.body, mailCampaign.job)
    messageSubject = merge_template(mailCampaign.message_template.subject, mailCampaign.job)

    # send to contacts
    emailAddresses = ['ajarvis@3gsllc.com']
    for vendorContact in mailCampaign.vendor_contacts.all():
        emailAddresses.append(vendorContact.user.email)

    email = EmailMultiAlternatives(
        messageSubject,
        messageBody,
        'jobs@1x3i.com',
        None,
        emailAddresses
    )

    for document in mailCampaign.job.documents.all():
        email.attach(document.display_name, document.document.path, 'application/msword')

    email.send()

    print "campaign started successfully"

    return HttpResponse(status=204)

def merge_template(template, job):
    # create the dataset
    data = {}
    data['job'] = job

    template = Template(template)
    context = Context(data)
    return template.render(context)