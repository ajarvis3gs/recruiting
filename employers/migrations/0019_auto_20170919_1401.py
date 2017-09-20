# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-09-19 14:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employers', '0018_auto_20170919_0008'),
    ]

    operations = [
        migrations.AddField(
            model_name='employerdocument',
            name='display_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='employerdocument',
            name='file_type',
            field=models.CharField(blank=True, choices=[(b'', b'Other'), (b'Task Order Form', b'Task Order Form'), (b'Candidate Response Form', b'Candidate Response Form')], max_length=100, null=True),
        ),
    ]
