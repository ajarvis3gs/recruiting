# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-09-18 14:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interviews', '0024_auto_20170918_1427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interviewinvitation',
            name='uuid',
            field=models.CharField(default=b'NBSLA', max_length=5, primary_key=True, serialize=False),
        ),
    ]
