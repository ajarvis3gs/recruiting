# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-09-19 12:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0013_auto_20170919_1204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobrequestedqualification',
            name='maximum_points',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='jobrequestedqualification',
            name='minimum_points',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
