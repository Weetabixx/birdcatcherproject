from django.contrib import admin

# Register your models here.

from twitter_stream.models import *
    
class TweetAdmin(admin.ModelAdmin): # lets you search for tweets on the admin page
    list_display=('tweet_text','tweet_handle','tweet_created','tweet_pin',)
    search_fields=['tweet_text','tweet_handle','tweet_created','tweet_pin']
    readonly_fields = ('tweet_handle', 'tweet_text', 'tweet_created',)
    
admin.site.register(tweet,TweetAdmin)
admin.site.register(account) 
admin.site.register(hashtag)
admin.site.register(group)