# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2018-05-10 12:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidates', '0006_candidate_initial_contact_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='best_contact_time',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name='candidate',
            name='preferred_communication_method',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
