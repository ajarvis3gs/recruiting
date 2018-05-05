from __future__ import unicode_literals

from django.db import models
from django.contrib.sites.models import Site


class SiteDetail(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    company_name = models.CharField(blank=True, null=True, max_length=100)
    logo = models.CharField(blank=True, null=True, max_length=100)
    support_email = models.CharField(blank=True, null=True, max_length=100)
    jobs_email = models.CharField(blank=True, null=True, max_length=100)
    info_email = models.CharField(blank=True, null=True, max_length=100)
    address = models.CharField(blank=True, null=True, max_length=100)
    phone = models.CharField(blank=True, null=True, max_length=100)


class SiteArticle(models.Model):
    sites = models.ManyToManyField(Site)
    content = models.TextField(blank=True, null=True)
    category = models.CharField(blank=True, null=True, max_length=100)
