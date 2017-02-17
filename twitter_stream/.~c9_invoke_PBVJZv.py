from __future__ import unicode_literals

from django.db import models


# Create your models here.

class tweet(models.Model):
    
    tweet_id = models.IntegerField(primary_key=True)
    
    tweet_handle = models.CharField(max_length=100)
    
    tweet_text = models.CharField(max_length=145)
    
    #tweet_profile_picture = models.CharField(max_length=2084)
    
    #tweet_expand_url = models.CharField(max_length=2084,blank=True)
    
    #tweet_image = models.CharField(max_length=2084,blank=True)
    
    tweet_created = models.CharField(max_length=100, null=True, blank=True)
    #twitter returns "created_at":"Wed Aug 27 13:08:45 +0000 2008"
    
    tweet_html = models.CharField(max_length=5000)
    
    try:
        
        def __unicode__(self):
            
            return self.tweet_text
    except ValueError:
        pass

class account(models.Model):
    
    account_id = models.IntegerField(primary_key=True)
    
    account_Name = models.CharField(max_length=100)
    
    account_handle = models.CharField(max_length=100)
    
    account_group = models.CharField(max_length=100, null=True,  blank = True)
    #to be implemented later
    
    try:
        def __unicode__(self):
            return self.account_Name
    except ValueError:
        pass
    
class hashtag(models.Model):
    
    hashtag_hash = models.CharField(primary_key=True, max_length=100)
    
    hashtag_group = models.CharField(primary_key=True, max)
    
    try:
        def __unicode__(self):
            return self.hashtag_hash
    except ValueError:
        pass
    
class group(models.Model):
    
    group_name = models.CharField(primary_key=True, max_length=100)
    
    group_level = models.IntegerField() 
    
    group_parent = models.CharField(max_length=100)
    
    try:
        def __unicode__(self):
            return self.group_name
    except ValueError:
        pass
    