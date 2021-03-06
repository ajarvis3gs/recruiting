# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-09-19 15:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0005_auto_20170919_1401'),
        ('campaigns', '0002_mailcampaign_mailcampaignvendorcontact'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mailcampaignvendorcontact',
            name='campaign',
        ),
        migrations.RemoveField(
            model_name='mailcampaignvendorcontact',
            name='vendor_contact',
        ),
        migrations.AddField(
            model_name='mailcampaign',
            name='vendor_contacts',
            field=models.ManyToManyField(to='vendors.VendorContact'),
        ),
        migrations.DeleteModel(
            name='MailCampaignVendorContact',
        ),
    ]
