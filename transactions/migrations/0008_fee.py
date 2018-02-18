# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-08 14:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0007_auto_20170307_1711'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('broker', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='transactions.Broker')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='transactions.Investor')),
            ],
        ),
    ]