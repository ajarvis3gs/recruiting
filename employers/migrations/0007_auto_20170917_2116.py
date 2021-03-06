# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-09-17 21:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employers', '0006_employerdocument'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employercontact',
            name='employer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contacts', to='employers.Employer'),
        ),
        migrations.AlterField(
            model_name='employerdocument',
            name='employer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='employers.Employer'),
        ),
    ]
