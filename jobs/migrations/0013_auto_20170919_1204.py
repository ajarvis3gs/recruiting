# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-09-19 12:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0012_job_target_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobrequestedqualification',
            name='maximum_points',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='jobrequestedqualification',
            name='minimum_points',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
    ]
