from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings
from localflavor.us.models import USStateField
from recruiting.choices import *

class Employer(models.Model):
    name = models.CharField(blank=False, max_length=200)
    code = models.CharField(blank=True, null=True, max_length=50)
    phone_number = models.CharField(blank=True, max_length=50) # PhoneNumberField(blank=False)
    fax_number = models.CharField(blank=True, max_length=50) # PhoneNumberField(blank=False)
    address = models.CharField(blank=True, max_length=200)
    address_2 = models.CharField(blank=True, max_length=200)
    city = models.CharField(blank=True, max_length=200)
    state = USStateField(blank=True)
    zip = models.CharField(blank=True, max_length=10)
    website = models.CharField(blank=True, max_length=200)
    notes = models.TextField(null=True, blank=True,)
    is_active = models.BooleanField(default=True)
    last_modified = models.DateTimeField(auto_now_add=False, auto_now=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.name

class EmployerContact(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='contacts')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    last_modified = models.DateTimeField(auto_now_add=False, auto_now=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return '%s <%s>' % (self.user.get_full_name(), self.user.email)

class EmployerDocument(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='documents')
    display_name = models.CharField(blank=True, null=True, max_length=100)
    file_type = models.CharField(blank=True, null=True, max_length=100, choices=FILE_TYPE_CHOICES)
    headers = models.TextField(null=True, blank=True,)
    document = models.FileField(upload_to=settings.ATTACHMENT_UPLOAD_TO,)
    last_modified = models.DateTimeField(auto_now_add=False, auto_now=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)


class EmployerPricingSchedule(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='pricingSchedules')
    region = models.IntegerField(choices=REGION_CHOICES)
    service_group = models.IntegerField(choices=SERVICE_GROUP_CHOICES)
    job_title = models.CharField(max_length=200, choices=JOB_TITLE_CHOICES)
    experience_level = models.CharField(blank=True, null=True, max_length=100, choices=EXPERIENCE_LEVEL_CHOICES)
    demand = models.CharField(blank=True, null=True, max_length=25, choices=DEMAND_CHOICES)
    hourly_wage = models.DecimalField(max_digits=5, decimal_places=2)
    hourly_rate = models.DecimalField(max_digits=5, decimal_places=2)
    is_active = models.BooleanField(default=True)
    last_modified = models.DateTimeField(auto_now_add=False, auto_now=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return '%s-%s-%s %s %s %s' % (self.employer.code, self.region, self.service_group, self.job_title, self.experience_level, self.demand)


def update_user_profile(sender, instance, created, **kwargs):
    from accounts.models import UserProfile
    if created:
        UserProfile.objects.filter(user=instance.user).update(user_type='Employer')

post_save.connect(update_user_profile, sender=EmployerContact)