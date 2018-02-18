# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-07 16:51
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('transactions', '0004_auto_20170307_0028'),
    ]

    operations = [
        migrations.CreateModel(
            name='FundsTransfer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fromBroker', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transferFrom', to='transactions.Broker')),
            ],
        ),
        migrations.CreateModel(
            name='Investor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currencyCode', models.CharField(max_length=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='transaction',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='transactions.Investor'),
        ),
        migrations.AddField(
            model_name='fundstransfer',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='transactions.Investor'),
        ),
        migrations.AddField(
            model_name='fundstransfer',
            name='toBroker',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transferTo', to='transactions.Broker'),
        ),
    ]