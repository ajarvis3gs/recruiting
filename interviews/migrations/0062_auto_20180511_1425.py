# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2018-05-11 14:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interviews', '0061_auto_20180511_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interviewinvitation',
            name='uuid',
            field=models.CharField(default=b'YRTGV', max_length=5, primary_key=True, serialize=False),
        ),
    ]
