# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-09-18 12:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20170918_1149'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='citizenship',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='skype_id',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='timezone',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
