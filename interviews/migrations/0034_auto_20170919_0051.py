# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-09-19 00:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interviews', '0033_auto_20170919_0046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interviewinvitation',
            name='uuid',
            field=models.CharField(default=b'QDHXZ', max_length=5, primary_key=True, serialize=False),
        ),
    ]
