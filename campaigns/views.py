from django.shortcuts import render
from campaigns.models import MailCampaign
import logging, os
from django.contrib import messages
from django.http import HttpResponse
from django.template import Template, Context
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib.sites.models import Site
from publicsite.models import SiteDetail
import re, cgi
from datetime import date, datetime
from campaigns.models import MailCampaign, MessageTemplate

logger = logging.getLogger(__name__)


def start_candidate_campaign(request, campaign_id):
    site = Site.objects.get_current()
    siteDetail = SiteDetail.objects.get(site=site)

    # load the campaign
    mailCampaign = MailCampaign.objects.get(id=campaign_id)

    messageCount = candidate_campaign(site, siteDetail, mailCampaign)

    mailCampaign.email_sent_date = datetime.now()
    mailCampaign.save()

    messages.add_message(request, messages.SUCCESS, '%s emails delivered successfully.' % messageCount)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def start_vendor_campaign(request, campaign_id):
    site = Site.objects.get_current()
    siteDetail = SiteDetail.objects.get(site=site)

    # load the campaign
    mailCampaign = MailCampaign.objects.get(id=campaign_id)

    tagless = re.compile(r'(<!--.*?-->|<[^>]*>)')
    textBody = tagless.sub('', mailCampaign.message_template.body)

    messageBody = merge_template(textBody, {'job': mailCampaign.job, 'site': site, 'siteDetail': siteDetail})
    messageSubject = merge_template(mailCampaign.message_template.subject, {'job': mailCampaign.job, 'site': site, 'siteDetail': siteDetail})

    # send to contacts
    emailAddresses = []

    # accumulate vendor contact email addresses (if existing)
    for vendorContact in mailCampaign.vendor_contacts.all():
        emailAddresses.append(vendorContact.user.email)

    email = EmailMultiAlternatives(
        messageSubject,
        messageBody,
        siteDetail.jobs_email,
        None,
        emailAddresses
    )

    for document in mailCampaign.job.documents.all():
        content = open(document.document.path, 'rb').read()
        email.attach(document.display_name, content)

    email.send()

    messages.add_message(request, messages.SUCCESS, '%s emails delivered successfully.' % len(emailAddresses))

    mailCampaign.email_sent_date = datetime.now()
    mailCampaign.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def merge_template(template, data):
    # create the dataset
    template = Template(template)
    context = Context(data)
    return template.render(context)


def candidate_campaign(site, siteDetail, mailCampaign):
    messageCount = 0

    # send to contacts
    for candidate in mailCampaign.candidates.all():
        job = mailCampaign.job
        if job is None and candidate.applications.count() > 0:
            job = candidate.applications.all()[0].job

        emailAddresses = [siteDetail.support_email, candidate.email]
        messageBody = merge_template(mailCampaign.message_template.body, {'candidate': candidate, 'job': job, 'site': site, 'siteDetail': siteDetail})
        messageSubject = merge_template(mailCampaign.message_template.subject, {'candidate': candidate, 'job': job, 'site': site, 'siteDetail': siteDetail})

        email = EmailMessage(
            messageSubject,
            messageBody,
            siteDetail.jobs_email,
            None,
            emailAddresses
        )

        email.content_subtype = "html"
        email.send()

        messageCount = messageCount + 1

        if mailCampaign.message_template.name == 'Candidate Response Form':
            candidate.response_form_sent_date = datetime.now()
            candidate.status='Awaiting Response Form'
            candidate.save()
        elif mailCampaign.message_template.name == 'Initial Candidate Contact':
            candidate.initial_contact_date = datetime.now()
            candidate.status='Contacted'
            candidate.save()
        elif mailCampaign.message_template.name == 'Inexperienced Candidate Response':
            candidate.status='Not Submitted - Inexperienced'
            candidate.save()
        elif mailCampaign.message_template.name == 'Unqualified Candidate Response':
            candidate.status='Not Submitted - Unqualified'
            candidate.save()
        elif mailCampaign.message_template.name == 'Position Filled Response':
            candidate.status='Not Submitted - Position Filled'
            candidate.save()

        mailCampaign.email_sent_date = datetime.now()
        mailCampaign.save()


    return messageCount


def initial_contact_campaign(job, candidate):
    messageTemplate = MessageTemplate.objects.get(name__exact='Initial Candidate Contact')

    campaign = MailCampaign(
        name = '%s %s Initial Contact Campaign' % (candidate.first_name, candidate.last_name),
        job = job,
        message_template = messageTemplate
    )
    campaign.save()

    campaign.candidates.add(candidate)

    return campaign


def response_form_campaign(job, candidate):
    messageTemplate = MessageTemplate.objects.get(name__exact='Candidate Response Form')

    campaign = MailCampaign(
        name = '%s %s Candidate Response Campaign' % (candidate.first_name, candidate.last_name),
        job = job,
        message_template = messageTemplate
    )
    campaign.save()

    campaign.candidates.add(candidate)

    return campaign