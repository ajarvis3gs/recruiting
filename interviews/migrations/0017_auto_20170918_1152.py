# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-09-18 11:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interviews', '0016_auto_20170918_1149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interviewinvitation',
            name='uuid',
            field=models.CharField(default=b'CMNVW', max_length=5, primary_key=True, serialize=False),
        ),
    ]
