# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2018-05-11 14:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interviews', '0058_auto_20180510_1342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interviewinvitation',
            name='uuid',
            field=models.CharField(default=b'76CIG', max_length=5, primary_key=True, serialize=False),
        ),
    ]
