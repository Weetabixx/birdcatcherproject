# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-23 13:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter_stream', '0021_auto_20170317_1852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='group_level',
            field=models.IntegerField(editable=False),
        ),
    ]
