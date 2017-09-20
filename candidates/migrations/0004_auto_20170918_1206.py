# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-09-18 12:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0002_auto_20170918_1152'),
        ('candidates', '0003_auto_20170918_1158'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='candidate',
            name='birth_year',
        ),
        migrations.RemoveField(
            model_name='candidate',
            name='current_location',
        ),
        migrations.AddField(
            model_name='candidate',
            name='vendor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='candidates', to='vendors.Vendor'),
        ),
    ]
