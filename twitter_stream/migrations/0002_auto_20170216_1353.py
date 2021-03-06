# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-02-16 13:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter_stream', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='account',
            fields=[
                ('account_id', models.IntegerField(primary_key=True, serialize=False)),
                ('account_Name', models.CharField(max_length=100)),
                ('account_handle', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='hashtag',
            fields=[
                ('hashtag_hash', models.CharField(max_length=100, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='tweet',
            fields=[
                ('tweet_id', models.IntegerField(primary_key=True, serialize=False)),
                ('tweet_handle', models.CharField(max_length=100)),
                ('tweet_text', models.CharField(max_length=145)),
                ('tweet_created', models.CharField(blank=True, max_length=100, null=True)),
                ('tweet_html', models.CharField(max_length=5000)),
            ],
        ),
        migrations.DeleteModel(
            name='tweets',
        ),
    ]
