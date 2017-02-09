from django.contrib import admin

# Register your models here.

from twitter_stream.models import *


admin.site.register(tweet)
admin.site.register(account)
admin.site.register(hashtag)