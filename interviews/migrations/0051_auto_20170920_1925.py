# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-09-20 19:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interviews', '0050_auto_20170919_2326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interviewinvitation',
            name='uuid',
            field=models.CharField(default=b'KG5NO', max_length=5, primary_key=True, serialize=False),
        ),
    ]
