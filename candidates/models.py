from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings
from vendors.models import Vendor
from recruiting.choices import *
from jobs.models import Job


class Candidate(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='candidates', blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=250, blank=True)
    last_name = models.CharField(max_length=250, blank=True)
    email = models.CharField(max_length=250, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(choices=(('male', 'Male'), ('female', 'Female'),), max_length=10, blank=True, null=True)
    education = models.CharField(
        max_length=25,
        blank=True,
        choices=EDUCATION_CHOICES,
    )
    education_major = models.CharField(max_length=250, blank=True)
    phone_number = models.CharField(blank=True, max_length=50)
    preferred_communication_method = models.CharField(max_length=100, blank=True)
    best_contact_time = models.CharField(max_length=250, blank=True)
    is_active = models.BooleanField(default=True)
    last_modified = models.DateTimeField(auto_now_add=False, auto_now=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    initial_contact_date = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)


class CandidateApplication(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='applications')
    job = models.ForeignKey(Job, related_name='applications')
    last_modified = models.DateTimeField(auto_now_add=False, auto_now=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return '%s %s Application' % (self.candidate.first_name, self.candidate.last_name)



class CandidateDocument(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='documents')
    display_name = models.CharField(blank=True, null=True, max_length=100)
    file_type = models.CharField(blank=True, null=True, max_length=100, choices=FILE_TYPE_CHOICES)
    headers = models.TextField(null=True, blank=True,)
    document = models.FileField(upload_to=settings.ATTACHMENT_UPLOAD_TO,)
    last_modified = models.DateTimeField(auto_now_add=False, auto_now=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
