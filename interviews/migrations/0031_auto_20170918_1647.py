# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-09-18 16:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interviews', '0030_auto_20170918_1641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interviewinvitation',
            name='uuid',
            field=models.CharField(default=b'SE9AP', max_length=5, primary_key=True, serialize=False),
        ),
    ]