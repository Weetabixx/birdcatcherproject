# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-02-03 18:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('twitter_stream', '0007_auto_20170201_1430'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hashtag',
            old_name='hashtag',
            new_name='hashtag_hash',
        ),
    ]
