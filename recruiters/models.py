from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models.signals import post_save

class Recruiter(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	is_active = models.BooleanField(default=True)
	last_modified = models.DateTimeField(auto_now_add=False, auto_now=True)
	created = models.DateTimeField(auto_now_add=True, auto_now=False)

	def __str__(self):
		return self.user.email


def update_user_profile(sender, instance, created, **kwargs):
	from accounts.models import UserProfile
	if created:
		UserProfile.objects.filter(user=instance.user).update(user_type='Recruiter')

post_save.connect(update_user_profile, sender=Recruiter)
