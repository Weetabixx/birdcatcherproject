# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-09 15:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter_stream', '0012_auto_20170309_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='tweet_pin',
            field=models.BooleanField(default=False),
        ),
    ]
