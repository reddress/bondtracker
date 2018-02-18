# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-07 00:06
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bonds', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Broker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('manager', models.CharField(max_length=80)),
                ('balance', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transactionDate', models.DateField()),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=6)),
                ('totalPrice', models.DecimalField(decimal_places=2, max_digits=10)),
                ('notes', models.CharField(max_length=80)),
                ('bond', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bonds.Bond')),
                ('broker', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='transactions.Broker')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TransactionType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('factor', models.IntegerField(default=1)),
            ],
        ),
    ]
