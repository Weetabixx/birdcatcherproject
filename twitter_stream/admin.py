from django.contrib import admin

# Register your models here.

from twitter_stream.models import *
    
admin.site.register(tweet)
admin.site.register(account) #removed ...  , account_Admin)
admin.site.register(hashtag)
admin.site.register(group)