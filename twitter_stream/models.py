from __future__ import unicode_literals

from django.db import models
from datetime import datetime

# Create your models here.

class tweet(models.Model):
    
    tweet_id = models.IntegerField(primary_key=True)
    
    tweet_handle = models.CharField(max_length=100)
    
    tweet_text = models.CharField(max_length=145)
    
    #twitter returns "created_at":"Wed Aug 27 13:08:45 +0000 2008"
    tweet_created = models.DateTimeField()
    
    tweet_html = models.CharField(max_length=5000)
    
    try:
        def __unicode__(self):
            return self.tweet_text
    except ValueError:
        pass

class account(models.Model):
    
    account_id = models.IntegerField(primary_key=True)
    
    account_Name = models.CharField(max_length=100)
    
    account_handle = models.CharField(max_length=100) #this assignment needs to trigger stream thread to restart
    
    account_group = models.CharField(max_length=100, null=True,  blank = True)
    
    account_filter = models.BooleanField(blank=False, null=False, default=True)
    #to be implemented later
    
    try:
        def __unicode__(self):
            return self.account_Name
    except ValueError:
        pass
    
class hashtag(models.Model):
    
    hashtag_hash = models.CharField(primary_key=True, max_length=100, null=False)
    
    hashtag_group = models.CharField(max_length=100, null=True)
    
    try:
        def __unicode__(self):
            return self.hashtag_hash
    except ValueError:
        pass
    
class group(models.Model):
    
    group_name = models.CharField(primary_key=True, max_length=100)
    
    group_level = models.IntegerField() 
    
    group_parent = models.CharField(max_length=100, null = True, blank = True)
    
    try:
        def __unicode__(self):
            return self.group_name
    except ValueError:
        pass
    