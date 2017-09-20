# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-09-17 14:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='accommodation_included',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='job',
            name='accommodation_stipend',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='compensation_amount',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='compensation_terms',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='compensation_type',
            field=models.CharField(blank=True, choices=[(b'One-time', b'One-time'), (b'Monthly', b'Monthly')], max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='contract_length',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='insurance_included',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='job',
            name='insurance_stipend',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='recruiter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to='recruiters.Recruiter'),
        ),
        migrations.AlterField(
            model_name='job',
            name='salary_high',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='salary_low',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='travel_stipend',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='weekly_hours',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
