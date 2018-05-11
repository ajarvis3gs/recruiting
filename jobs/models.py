from django.db import models

from recruiters.models import Recruiter
from employers.models import Employer, EmployerContact, EmployerPricingSchedule
from django.conf import settings
from recruiting.choices import *

class Country(models.Model):
    country = models.CharField(
        max_length=100,
    )

    def __str__(self):
        return self.country

class Job(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=100)
    employer_contact = models.ForeignKey(EmployerContact, related_name='jobs', null=True)
    pricing_schedule = models.ForeignKey(EmployerPricingSchedule, related_name='jobs', null=True)
    agency = models.CharField(blank=True, null=True, max_length=100)
    location = models.CharField(blank=True, null=True, max_length=100)
    target_rate = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2)
    vendor_rate = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2)
    submission_date = models.DateField(blank=True, null=True)
    vendor_submission_date = models.DateField(blank=True, null=True)
    total_positions = models.IntegerField(blank=True, null=True)
    max_submissions = models.IntegerField(blank=True, null=True)
    preferred_hardware = models.CharField(blank=True, null=True, max_length=500)
    preferred_software = models.CharField(blank=True, null=True, max_length=500)
    work_hours = models.CharField(blank=True, null=True, max_length=255)
    description = models.TextField(null=True, blank=True,)
    is_featured = models.BooleanField(default=False, verbose_name='Published')
    is_active = models.BooleanField(default=True)
    last_modified = models.DateTimeField(auto_now_add=False, auto_now=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return "%s: %s" % (self.id, self.title)

class JobMandatoryQualification(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='mandatoryQualifications')
    label = models.TextField(null=True, blank=True)

class JobRequestedQualification(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='requestedQualifications')
    qualification_number = models.CharField(null=True, blank=True, max_length=10)
    label = models.TextField(null=True, blank=True)
    minimum_points = models.CharField(blank=True, null=True, max_length=10)
    maximum_points = models.CharField(blank=True, null=True, max_length=10)

class JobAdditionalInformationRequest(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='additionalInformationRequests')
    label = models.TextField(null=True, blank=True)
    value = models.TextField(null=True, blank=True,)

class JobDocument(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='documents')
    display_name = models.CharField(blank=True, null=True, max_length=100)
    file_type = models.CharField(blank=True, null=True, max_length=100, choices=FILE_TYPE_CHOICES)
    headers = models.TextField(null=True, blank=True,)
    document = models.FileField(upload_to=settings.ATTACHMENT_UPLOAD_TO,)
    last_modified = models.DateTimeField(auto_now_add=False, auto_now=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
