# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-09-19 21:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0017_job_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='preferred_hardware',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='preferred_software',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='work_hours',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
