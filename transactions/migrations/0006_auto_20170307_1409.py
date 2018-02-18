# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-07 17:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0005_auto_20170307_1351'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='advertisedReturn',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='notes',
            field=models.CharField(blank=True, max_length=80),
        ),
    ]