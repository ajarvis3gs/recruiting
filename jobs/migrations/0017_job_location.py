# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-09-19 16:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0016_auto_20170919_1444'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='location',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
