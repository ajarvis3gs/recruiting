# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-09-16 18:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruiters', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recruiter',
            name='date_of_birth',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='recruiter',
            name='image',
            field=models.ImageField(blank=True, upload_to=b'recruiter/%Y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='recruiter',
            name='location',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='recruiter',
            name='phone_number',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
