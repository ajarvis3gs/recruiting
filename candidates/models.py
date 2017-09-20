from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings
from vendors.models import Vendor
from recruiting.choices import *


class Candidate(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='candidates', blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(choices=(('male', 'Male'), ('female', 'Female'),), max_length=10, blank=True, null=True)
    education = models.CharField(
        max_length=25,
        blank=True,
        choices=EDUCATION_CHOICES,
    )
    education_major = models.CharField(max_length=250, blank=True)
    is_active = models.BooleanField(default=True)
    last_modified = models.DateTimeField(auto_now_add=False, auto_now=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return '%s: %s' % (self.vendor.name, self.user.get_full_name())


def update_user_profile(sender, instance, created, **kwargs):
    from accounts.models import UserProfile
    if created:
        UserProfile.objects.filter(user=instance.user).update(user_type='Candidate')


post_save.connect(update_user_profile, sender=Candidate)


class CandidateDocument(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='documents')
    display_name = models.CharField(blank=True, null=True, max_length=100)
    file_type = models.CharField(blank=True, null=True, max_length=100, choices=FILE_TYPE_CHOICES)
    headers = models.TextField(null=True, blank=True,)
    document = models.FileField(upload_to=settings.ATTACHMENT_UPLOAD_TO,)
    last_modified = models.DateTimeField(auto_now_add=False, auto_now=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
