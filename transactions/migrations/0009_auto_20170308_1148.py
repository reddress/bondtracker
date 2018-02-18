# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-08 14:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0008_fee'),
    ]

    operations = [
        migrations.AddField(
            model_name='fee',
            name='feeDate',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fee',
            name='notes',
            field=models.CharField(blank=True, max_length=80),
        ),
    ]