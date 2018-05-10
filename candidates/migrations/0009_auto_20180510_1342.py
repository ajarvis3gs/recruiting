# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2018-05-10 13:42
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('candidates', '0008_auto_20180510_1333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
