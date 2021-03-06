# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-09 14:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter_stream', '0010_auto_20170302_1835'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='tweet_pin',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='account',
            name='account_group',
            field=models.CharField(blank=True, choices=[('testgroup', 'testgroup'), ('Aberdeen_University', 'Aberdeen_University'), ('Aberdeen_HSRU', 'Aberdeen_HSRU'), ('Aberdeen_COPS', 'Aberdeen_COPS'), ('Aberdeen_CLSM', 'Aberdeen_CLSM'), ('Aberdeen_CASS', 'Aberdeen_CASS'), ('groupgroup', 'groupgroup')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='hashtag',
            name='hashtag_group',
            field=models.CharField(choices=[('testgroup', 'testgroup'), ('Aberdeen_University', 'Aberdeen_University'), ('Aberdeen_HSRU', 'Aberdeen_HSRU'), ('Aberdeen_COPS', 'Aberdeen_COPS'), ('Aberdeen_CLSM', 'Aberdeen_CLSM'), ('Aberdeen_CASS', 'Aberdeen_CASS'), ('groupgroup', 'groupgroup')], max_length=100, null=True),
        ),
    ]
