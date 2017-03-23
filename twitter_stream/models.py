from __future__ import unicode_literals

from django.db import models
from datetime import datetime
from django.contrib.postgres.fields import ArrayField
from smart_selects.db_fields import ChainedForeignKey


class group(models.Model):
    
    group_name = models.CharField(primary_key=True, max_length=100)
    group_level = models.IntegerField(editable=False) 
    group_parent = models.ForeignKey("group", null = True, blank = True) 
    
    def save(self): # auto add group level to be one higher than parent group
        if self.group_parent == None:
            self.group_level = 0
        else:
            self.group_level = self.group_parent.group_level + 1 #ignore this error, it works
        super(group, self).save()
    
    try:
        def __unicode__(self):
            return self.group_name
    except ValueError:
        pass
    
class tweet(models.Model):
    
    tweet_id = models.IntegerField(primary_key=True, editable=False)
    tweet_handle = models.CharField(max_length=100, editable=False)
    tweet_text = models.CharField(max_length=145, editable=False)
    tweet_created = models.DateTimeField(editable=False)
    tweet_html = models.CharField(max_length=5000, editable=False)
    tweet_pin = models.CharField(max_length=100, null=True,  blank = True)
    
    try:
        def __unicode__(self):
            return self.tweet_text
    except ValueError:
        pass
    
class account(models.Model):
    
    account_id = models.AutoField(primary_key=True)
    account_Name = models.CharField(max_length=100)
    account_handle = models.CharField(max_length=100) #this assignment needs to trigger stream thread to restart
    account_group = models.ForeignKey("group", null=True,  blank = True)
    filter_by_hashtags = models.BooleanField(blank=False, null=False, default=True)
    
    try:
        def __unicode__(self):
            return self.account_Name
    except ValueError:
        pass

class hashtag(models.Model):
    
    hashtag_hash = models.CharField(primary_key=True, max_length=100, null=False)
    hashtag_group = models.ForeignKey("group", null=True,  blank = True)
    
    try:
        def __unicode__(self):
            return self.hashtag_hash
    except ValueError:
        pass
