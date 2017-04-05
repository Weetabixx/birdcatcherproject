from django.contrib import admin

# Register your models here.

from twitter_stream.models import *
    
class TweetAdmin(admin.ModelAdmin): # lets you search for tweets on the admin page
    list_display=('tweet_text','tweet_handle','tweet_created','tweet_pin',)
    search_fields=['tweet_text','tweet_handle','tweet_created','tweet_pin']
    readonly_fields = ('tweet_handle', 'tweet_text', 'tweet_created',)
    
class AccountAdmin(admin.ModelAdmin): # lets you search for tweets on the admin page
    list_display=('account_handle','account_Name','account_group','filter_by_hashtags',)
    search_fields=['account_handle','account_Name','account_group__group_name']
    readonly_fields = ('account_handle','account_Name')
    
admin.site.register(tweet,TweetAdmin)
admin.site.register(account,AccountAdmin) 
admin.site.register(hashtag)
admin.site.register(group)