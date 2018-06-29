from django_mailbox.signals import message_received
from django_mailbox.models import MessageAttachment
from django.dispatch import receiver
import os, re, logging
from django.conf import settings
from datetime import datetime, timedelta
from jobs.models import Job, JobDocument, JobMandatoryQualification, JobRequestedQualification, JobAdditionalInformationRequest
from employers.models import Employer, EmployerContact, EmployerPricingSchedule
from employers.models import EmployerPricingSchedule
from campaigns.models import MailCampaign, MessageTemplate
import zipfile
from decimal import Decimal
from xml.etree.cElementTree import XML
from django.core.exceptions import *
import xmlrpclib
import base64


WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
PARA = WORD_NAMESPACE + 'p'
TEXT = WORD_NAMESPACE + 't'

logger = logging.getLogger(__name__)

@receiver(message_received)
def message_received(sender, message, **args):
    # let's figure out what email account this came in on
    from_address = message.from_address[0]

    try:
        logger.error("searching for employer contact %s" % from_address)
        employerContact = EmployerContact.objects.get(user__email=from_address)
        employer = employerContact.employer

        # TODO:
        # what should we do if we can't find a contact?
        # figure out what type of email this is.  for now we'll assume it's a job listing

        # extract job details from message body
        title = findJobTitle(message.subject)
        targetRate = findTargetRate(message.text)
        submissionDate = findSubmissionDate(message.text)
        vendorSubmissionDate = submissionDate - timedelta(days=2)
        replyToContact = findReplyToContact(message.text)

        logger.error("creating new job...")
        logger.error("employer: %s" % employer.name)
        logger.error("title: %s" % title)
        logger.error("targetRate: %s" % targetRate)
        logger.error("submissionDate: %s" % submissionDate)
        logger.error("vendorSubmissionDate: %s" % vendorSubmissionDate)
        logger.error("replyToContact: %s" % replyToContact)

        # create the job
        job = Job(
            employer = employer,
            title = title,
            target_rate = targetRate,
            submission_date = submissionDate,
            vendor_submission_date = vendorSubmissionDate,
            employer_contact=replyToContact
        )
        job.save()

        # create the campaign but don't start it just yet
        messageTemplate = MessageTemplate.objects.get(name__exact='Single HBITS Opportunity Template')

        campaign = MailCampaign(
            name = '%s Campaign' % job.title,
            job = job,
            message_template = messageTemplate
        )
        # temporarily disabling campaign creation for vendors
        # campaign.save()

        # associate the attachments
        attachments = MessageAttachment.objects.filter(message_id=message.id)
        for attachment in attachments:
            jobDocument = JobDocument(job=job, headers=attachment.headers, document=attachment.document)
            jobDocument.display_name = findDocumentName(attachment.headers)
            jobDocument.save()

            # extract job details from attachments
            parsedAttachment = parseAttachment(attachment.document.name)

            jobDocument.file_type = parsedAttachment['formType']
            jobDocument.save()

            if (parsedAttachment['formType'] == 'Task Order Form'):
                logger.error("parsing task order form...")

                job.max_submissions = parsedAttachment['maxSubmissions']
                job.agency = parsedAttachment['agency']
                job.location = parsedAttachment['location']
                job.total_positions = parsedAttachment['totalPositions']
                job.description = parsedAttachment['description']
                job.preferred_hardware = parsedAttachment['preferredHardware']
                job.preferred_software = parsedAttachment['preferredSoftware']
                job.work_hours = parsedAttachment['workHours']

                logger.error("maxSubmissions: %s" % job.max_submissions)
                logger.error("agency: %s" % job.agency)
                logger.error("location: %s" % job.location)
                logger.error("totalPositions: %s" % job.total_positions)
                logger.error("preferredHardware: %s" % job.preferred_hardware)
                logger.error("preferredSoftware: %s" % job.preferred_software)
                logger.error("workHours: %s" % job.work_hours)

                # try to determine the pricing schedule.  we still need the service group and region
                pricingSchedule = findPricingSchedule(employer, parsedAttachment)
                if pricingSchedule:
                    rateSpread = job.target_rate - pricingSchedule.hourly_wage
                    vendorRate = pricingSchedule.hourly_wage + (rateSpread / 2)

                    job.pricing_schedule = pricingSchedule
                    job.vendor_rate = vendorRate

                    logger.error("pricingSchedule: %s" % pricingSchedule)
                    logger.error("vendorRate: %s" % vendorRate)

                job.save()

                # save mandatory requirements
                if parsedAttachment['mandatoryQualifications']:
                    mandatory = JobMandatoryQualification(
                            job = job,
                            label = parsedAttachment['mandatoryQualifications']
                    )
                    mandatory.save()

                # save requested qualifications
                for requestedQualification in parsedAttachment['requestedQualifications'].values():
                    requested = JobRequestedQualification(
                        job = job,
                        qualification_number = requestedQualification['qualificationNumber'],
                        label = requestedQualification['label'],
                        minimum_points = requestedQualification['minimumPoints'],
                        maximum_points = requestedQualification['maximumPoints']
                    )
                    requested.save()

                # save additional info
                for additionalInformationRequest in parsedAttachment['additionalInformationRequests'].values():
                    info = JobAdditionalInformationRequest(
                        job = job,
                        label = additionalInformationRequest['label'],
                        value = additionalInformationRequest['value']
                    )
                    info.save()

        # finally, create the appropriate records in our crm system
        startPipeline(job.id)

        logger.error("message creation complete")
    except:
        logger.error("error processing new message")

def startPipeline(job_id):
    job = Job.objects.get(id=job_id)

    # authenticate
    common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(settings.ODOO_SERVER_URL))
    uid = common.authenticate(settings.ODOO_SERVER_DATABASE, settings.ODOO_SERVER_USERNAME, settings.ODOO_SERVER_PASSWORD, {})

    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(settings.ODOO_SERVER_URL))

    # check to see if this job exists already
    count = models.execute_kw(settings.ODOO_SERVER_DATABASE, uid, settings.ODOO_SERVER_PASSWORD, 'hr.job', 'search_count',
                              [[['name', '=', "%s" % (job.title)]]])

    # create a new job
    if count == 0:
        id = models.execute_kw(settings.ODOO_SERVER_DATABASE, uid, settings.ODOO_SERVER_PASSWORD, 'hr.job', 'create', [{
            'name': "%s" % (job.title),
            'description': '%s' % job.description
        }])

        for attachment in job.documents.all():
            file = attachment.document.file
            file.open(mode='rb')
            lines = file.read()
            file.close()

            id = models.execute_kw(settings.ODOO_SERVER_DATABASE, uid, settings.ODOO_SERVER_PASSWORD, 'ir.attachment', 'create', [{
                'res_model': 'hr.job',
                'res_id': id,
                'name': "%s" % attachment.display_name,
                'display_name': "%s" % attachment.display_name,
                'datas_fname': "%s" % attachment.display_name,
                'store_fname': "%s" % attachment.display_name,
                'type': 'binary',
                'datas': base64.b64encode(lines)
            }])


def findJobTitle(text):
    text = text.replace('URGENT REQUIREMENT', '')
    text = text.replace('URGENT NEW REQUIREMENT', '')
    text = text.replace('URGENT Requirement', '')
    text = text.replace('NEW REQUIREMENT', '')
    text = text.replace('New Requirement', '')
    text = text.replace('REQUIREMENT', '')
    text = text.replace('Requirement', '')
    text = text.replace('; ', '')

    return text

def findDocumentName(text):
    match = re.search('filename=\".*?\"', text)
    if not match:
        return text

    match = match.group(0)
    match = match.replace('filename=', '')
    match = match.replace('"', '')
    return match

def findRegion(text):
    match = re.search('(\d)+', text)
    if not match:
        if 'one' in text:
            return 1
        elif 'two' in text:
            return 2
        elif 'three' in text:
            return 3
        else:
            return text

    match = match.group(0)
    return match

def findServiceGroup(text):
    match = re.search('(\d)+', text)
    if not match:
        if 'one' in text:
            return 1
        elif 'two' in text:
            return 2
        else:
            return text

    match = match.group(0)
    return match

def findReplyToContact(text):
    match = re.findall('[a-zA-Z\.-]+@[\w\.-]+', text)
    match = match[-1]
    return EmployerContact.objects.get(user__email=match)

def findSubmissionDate(text):
    match = re.search('No later than:.*(\d)+/(\d)+/(\d)+', text)
    if not match:
        return text

    match = match.group(0)
    match = match.replace('No later than:','')
    patterns = ['%m/%d/%Y','%m/%d/%y','%m/%e/%Y','%m/%e/%y']
    for pattern in patterns:
        try:
            return datetime.strptime(match.strip(), pattern)
        except ValueError:
            logger.error("Unable to parse date using format: %s" % pattern)

def findTargetRate(text):
    match = re.search('\$.*hour', text)
    if not match:
        return text

    match = match.group(0)
    match = match.replace('$','')
    match = match.replace('/','')
    match = match.replace('hour','')
    match = match.replace('hr','')
    return Decimal(match.strip())

def findPricingSchedule(employer, values):
    region = findRegion(values['region'])
    serviceGroup = findServiceGroup(values['serviceGroup'])
    demand = values['demand']
    experienceLevel = values['experienceLevel'].replace('-',' ')
    jobTitle = values['jobTitle']

    try:
        return EmployerPricingSchedule.objects.get(
            employer_id = employer.id,
            region = region,
            service_group = serviceGroup,
            job_title = jobTitle,
            experience_level = experienceLevel,
            demand = demand
        )
    except ObjectDoesNotExist:
        return None


def parseAttachment(filename):
    print 'parsing file %s' % filename

    mandatoryQualificationsStart = 0
    mandatoryQualificationsEnd = 0
    requestedQualificationsStart = 0
    requestedQualificationsEnd = 0
    additionalInformationRequestsStart = 0

    document = zipfile.ZipFile(os.path.join(settings.MEDIA_ROOT, filename))
    xml_content = document.read('word/document.xml')
    document.close()
    tree = XML(xml_content)

    texts = []
    for paragraph in tree.getiterator(PARA):
        texts.append([node.text
                      for node in paragraph.getiterator(TEXT)
                      if node.text])

    parsedValues = {}
    parsedValues['formType'] = ''
    parsedValues['mandatoryQualifications'] = ''
    parsedValues['workHours'] = ''
    parsedValues['preferredHardware'] = ''
    parsedValues['preferredSoftware'] = ''
    parsedValues['location'] = ''
    parsedValues['requestedDate'] = ''
    parsedValues['agency'] = ''
    parsedValues['serviceGroup'] = ''
    parsedValues['totalPositions'] = ''
    parsedValues['jobTitle'] = ''
    parsedValues['demand'] = ''
    parsedValues['experienceLevel'] = ''
    parsedValues['maxSubmissions'] = '0'
    parsedValues['startDate'] = ''
    parsedValues['engagementLength'] = ''
    parsedValues['endDate'] = ''
    parsedValues['region'] = ''
    parsedValues['description'] = ''

    for i in range(0, len(texts)):
        if texts[i]:
            currentText = ''.join(texts[i])
            if 'Form 1:' in currentText:
                parsedValues['formType'] = 'Task Order Form'
            if 'Form 2:' in currentText:
                parsedValues['formType'] = 'Candidate Response Form'
            if 'Request Date:' in currentText:
                parsedValues['requestedDate'] = ''.join(texts[i+1]).strip()
            elif 'Agency:' in currentText:
                parsedValues['agency'] = ''.join(texts[i+1]).strip()
            elif 'Which Service Group is required' in currentText:
                parsedValues['serviceGroup'] = ''.join(texts[i+1]).strip()
            elif 'What is the number of staff being requested' in currentText:
                parsedValues['totalPositions'] = ''.join(texts[i+2]).strip()
            elif 'Which Job Title Category is required' in currentText:
                parsedValues['jobTitle'] = ''.join(texts[i+1]).strip()
            elif 'Which Skill Level is required' in currentText:
                parsedValues['experienceLevel'] = ''.join(texts[i+1]).strip()
            elif 'Which Skill Demand is required' in currentText:
                parsedValues['demand'] = ''.join(texts[i+1]).strip()
            elif 'How many Candidate Response Forms are being requested per Contractor per position' in currentText:
                parsedValues['maxSubmissions'] = ''.join(texts[i+1]).strip()
            elif 'When is the Target Start Date' in currentText:
                parsedValues['startDate'] = ''.join(texts[i+2]).strip()
            elif 'How long is the engagement' in currentText:
                parsedValues['engagementLength'] = ''.join(texts[i+1]).strip()
            elif 'When is the estimated completion date' in currentText:
                parsedValues['endDate'] = ''.join(texts[i+1]).strip()
            elif 'Where is the Home Base Region' in currentText:
                parsedValues['region'] = ''.join(texts[i+1]).strip()
            elif 'Where is the work office located' in currentText:
                parsedValues['location'] = ''.join(texts[i+1]).strip()
            elif 'What type of software is typically used by the Agency' in currentText:
                parsedValues['preferredSoftware'] = ''.join(texts[i+1]).strip()
            elif 'What type of hardware is typically used by the Agency' in currentText:
                parsedValues['preferredHardware'] = ''.join(texts[i+1]).strip()
            elif 'Please provide a full listing of the day to day tasks' in currentText:
                parsedValues['description'] = ''.join(texts[i+1]).strip()
            elif 'What are the daily work hours' in currentText:
                parsedValues['workHours'] = ''.join(texts[i+1]).strip()
            elif 'Position Mandatory Qualifications' in currentText:
                mandatoryQualificationsStart = i
                parsedValues['mandatoryQualifications'] = ''
            elif 'Qualifications cannot be changed' in currentText:
                mandatoryQualificationsEnd = i
            elif 'Maximum Points Allowed for Exceeding Qualifications' in currentText:
                requestedQualificationsStart = i
            elif 'Requested Qualifications Must Always Total 80' in currentText:
                requestedQualificationsEnd = i
            elif 'Additional Information Requests' in currentText:
                additionalInformationRequestsStart = i

    # parse the mandatory qualifications
    if mandatoryQualificationsStart > 0:
        for i in range (mandatoryQualificationsStart, mandatoryQualificationsEnd-2):
            if texts[i]:
                parsedValues['mandatoryQualifications'] += ''.join(texts[i+1]) + '\r\n'

    # parse the requested qualifications
    if requestedQualificationsStart > 0:
        requestedQualifications = {}
        count = 0
        for i in range (requestedQualificationsStart+1, requestedQualificationsEnd-4, 4):
            qualificationNumber = ''.join(texts[i+2])
            label = ''.join(texts[i+3])
            minimumPoints = ''.join(texts[i+4])
            maximumPoints = ''.join(texts[i+5])
            count = count + 1

            requestedQualifications[count] = {}
            requestedQualifications[count]['qualificationNumber'] = qualificationNumber if qualificationNumber else ''
            requestedQualifications[count]['label'] = label if label else ''
            requestedQualifications[count]['minimumPoints'] = minimumPoints if minimumPoints else ''
            requestedQualifications[count]['maximumPoints'] = maximumPoints if maximumPoints else ''

        parsedValues['requestedQualifications'] = requestedQualifications

    # parse the additional information requests
    if additionalInformationRequestsStart > 0:
        additionalInformationRequests = {}
        count = 0
        for i in range (additionalInformationRequestsStart, len(texts)-2, 2):
            count = count + 1
            label = ''.join(texts[i+1])
            value = ''.join(texts[i+2])

            if label:
                additionalInformationRequests[count] = {}
                additionalInformationRequests[count]['label'] = label if label else ''
                additionalInformationRequests[count]['value'] = value if value else ''

        parsedValues['additionalInformationRequests'] = additionalInformationRequests

    return parsedValues