# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2018-05-10 11:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidates', '0005_auto_20170919_1401'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='initial_contact_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
