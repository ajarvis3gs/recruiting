from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core import signing
from django.core.signing import SignatureExpired, BadSignature
from localflavor.us.models import USStateField

from django_countries.fields import CountryField
from allauth.account.models import EmailAddress

from recruiting.choices import (TIMEZONE_CHOICES, COUNTRY_CHOICES, GENDER_CHOICES,
                                EDUCATION_CHOICES, EMPLOYER_TYPE_CHOICES, POSITION_TYPE_CHOICES,
                                DESIRED_MONTHLY_SALARY_CHOICES)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(
        choices=(
            ('Candidate', 'Candidate'), ('Recruiter', 'Recruiter'), ('Employer', 'Employer'), ('Vendor', 'Vendor'),),
        max_length=50,
    )
    title = models.CharField(blank=True, max_length=100)
    phone_number = models.CharField(blank=True, max_length=50) # PhoneNumberField(blank=False)
    fax_number = models.CharField(blank=True, max_length=50) # PhoneNumberField(blank=False)
    notes = models.TextField(null=True, blank=True,)
    last_modified = models.DateTimeField(auto_now_add=False, auto_now=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.user.email

    def generate_token(self):
        email = self.user.email
        token = signing.dumps({'email': email})
        return token

    @staticmethod
    def verify_token(token, max_age=604800):
        # default max_age is 7 days
        try:
            value = signing.loads(token, max_age=max_age)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        user = User.objects.get(email=value['email'])
        return user


def create_account_emailaddress(sender, instance, created, **kwargs):
    # Used for django-allauth
    if created:
        EmailAddress.objects.get_or_create(
            user_id=instance.id,
            email=instance.email
        )


post_save.connect(create_account_emailaddress, sender=User)
