import logging
import os
import re
from datetime import datetime, timedelta
from django.conf import settings
from employers.models import Employer, EmployerPricingSchedule, EmployerContact
import zipfile
from xml.etree.cElementTree import XML
from django.core.mail import EmailMessage

logger = logging.getLogger(__name__)

WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
PARA = WORD_NAMESPACE + 'p'
TEXT = WORD_NAMESPACE + 't'

def updateEmployerPricingSchedules():
    print 'updating pricing schedules'
    EmployerPricingSchedule.objects.all().update(demand='Normal')

def cloneEmployeePricingSchedules():
    print 'cloning pricing schedules'
    pricingSchedules = EmployerPricingSchedule.objects.all()
    for pricingSchedule in pricingSchedules:
        if (pricingSchedule.service_group == 1):
            pricingSchedule.pk = None
            pricingSchedule.demand = 'High'
            pricingSchedule.save()

def findReplyToContact(text):
    match = re.findall('[a-zA-Z\.-]+@[\w\.-]+', text)
    match = match[-1]
    return EmployerContact.objects.get(user__email=match)

def findServiceGroup(text):
    match = re.search('(\d)+', text).group(0)
    return match

def findRegion(text):
    match = re.search('(\d)+', text).group(0)
    return match

def findDocumentName(text):
    match = re.search('filename=\".*?\"', text).group(0)
    match = match.replace('filename=', '')
    match = match.replace('"', '')
    return match


def findTargetRate(text):
    match = re.search('\$.*hour', text)
    if not match:
        return text
    match = match.group(0)
    match = match.replace('$','')
    match = match.replace('/','')
    match = match.replace('hour','')
    return match.strip()

def findSubmissionDate(text):
    match = re.search('No later than:.*(\d)+/(\d)+/(\d)+', text).group(0)
    match = match.replace('No later than:','')
    patterns = ['%m/%d/%Y','%m/%d/%y','%m/%e/%Y','%m/%e/%y']
    for pattern in patterns:
        try:
            return datetime.strptime(match.strip(), pattern)
        except ValueError:
            logger.error("Unable to parse date using format: %s" % pattern)

def run():
    print findTargetRate('$70.00 / hour')