# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-02-16 15:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter_stream', '0002_auto_20170216_1353'),
    ]

    operations = [
        migrations.CreateModel(
            name='group',
            fields=[
                ('group_name', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('group_level', models.IntegerField()),
                ('group_parent', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='account',
            name='account_group',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='hashtag',
            name='hashtag_group',
            field=models.CharField(max_length=100, null=True),
        ),
    ]