# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-09-19 21:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruiters', '0003_auto_20170916_1854'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recruiter',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
    ]