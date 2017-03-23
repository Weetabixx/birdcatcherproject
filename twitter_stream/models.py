from __future__ import unicode_literals

from django.db import models
from datetime import datetime
from django.contrib.postgres.fields import ArrayField
#from smart_selects.db_fields import ChainedForeignKey have to add this to INSTALLED_APPS
# Create your models here.

    
class group(models.Model):
    
    group_name = models.CharField(primary_key=True, max_length=100)
    
    group_level = models.IntegerField() 
    
    group_parent = models.ForeignKey("group", null = True, blank = True) 
    
    try:
        def __unicode__(self):
            return self.group_name
    except ValueError:
        pass
    
class tweet(models.Model):
    
    tweet_id = models.IntegerField(primary_key=True, editable=False)
    
    tweet_handle = models.CharField(max_length=100, editable=False)
    
    tweet_text = models.CharField(max_length=145, editable=False)
    
    #twitter returns "created_at":"Wed Aug 27 13:08:45 +0000 2008"
    tweet_created = models.DateTimeField(editable=False)
    
    tweet_html = models.CharField(max_length=5000, editable=False)
    
    tweet_pin = models.CharField(max_length=100, null=True,  blank = True)
    
    #tweet_pin = models.CharField(max_length=100, null=True,  blank = True, choices=[(x.group_name,x.group_name) for x in group.objects.all()])
    
    try:
        def __unicode__(self):
            return self.tweet_text
    except ValueError:
        pass
    
class account(models.Model):
    
    #auto_increment_id = models.AutoField(primary_key=True)
    
    account_id = models.AutoField(primary_key=True)
    
    account_Name = models.CharField(max_length=100)
    
    account_handle = models.CharField(max_length=100) #this assignment needs to trigger stream thread to restart
    
    #Group_Choices =[(x.group_name,x.group_name) for x in group.objects.all()]
    
    account_group = models.ForeignKey("group", null=True,  blank = True)
    
    #account_group = models.CharField(max_length=100, null = True)
    
    #account_group = models.CharField(max_length=100, null=True,  blank = True, choices=[(x.group_name,x.group_name) for x in group.objects.all()])
    
    filter_by_hashtags = models.BooleanField(blank=False, null=False, default=True)
    
    #def __init__(self, *args, **kwargs):
    #    super(account,self).__init__(*args, **kwargs)
    #    self.fields['account_group'].choices = [(x.group_name,x.group_name) for x in group.objects.all()]
    
    try:
        def __unicode__(self):
            return self.account_Name
    except ValueError:
        pass

class hashtag(models.Model):
    
    hashtag_hash = models.CharField(primary_key=True, max_length=100, null=False)
    
    hashtag_group = models.ForeignKey("group", null=True,  blank = True)
    
    #hashtag_group = models.CharField(max_length=100, null=True, choices=[(x.group_name,x.group_name) for x in group.objects.all()])
    
    try:
        def __unicode__(self):
            return self.hashtag_hash
    except ValueError:
        pass
