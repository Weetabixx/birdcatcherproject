# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-16 15:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter_stream', '0016_auto_20170316_1539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='account_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
