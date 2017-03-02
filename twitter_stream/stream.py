# -*- coding: utf-8 -*-

try:
         import json
except ImportError:
        import simplejson as json

        
from .models import tweet
from .models import account
from .models import hashtag
from twitter import Twitter, OAuth, TwitterHTTPError,TwitterStream
import oembed
from datetime import datetime
import time
from dateutil import parser
import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import os
from threading import Thread
import threading
import requests.packages.urllib3
from django.db import transaction
requests.packages.urllib3.disable_warnings()


# Variables that contains the user credentials to access Twitter API
ACCESS_TOKEN = '235228993-UMgntnuS8UKyGU7pitxvMNxQO4Eqte2tgAGk9ijK'
ACCESS_SECRET = '9I8YOVtb6zIZaPpQEnAdVOZaq6vNBZJZVaRiU2OZir8os'
CONSUMER_KEY = 'pPa5GLuxOLzK57woQ1pdYQIAf'
CONSUMER_SECRET = 'IAsBqLL6lOQdcZ4VRu1ZIPvTOMIDw2Pa4bMbPtXbxP8Xwkjjd6'

#Establish connection to twitter for embedded tweet
consumer = oembed.OEmbedConsumer()
endpoint = oembed.OEmbedEndpoint('https://publish.twitter.com/oembed?', 'https://twitter.com/*' )
consumer.addEndpoint(endpoint)

#function to retrieve embedded tweet
def embed_tweet(tweet_id,tweet_handle):
    response = consumer.embed("https://twitter.com/"+tweet_handle+"/status/" + str(tweet_id))
    html_tweet = response["html"]
    return html_tweet

#stores a tweet in the database and retrieves an embedded html code
def store_tweet(status):
    '''
    add the hashtags here, crosscheck received tweets with the hashtags stored in the database
    hashtag table should contain the hashtag itself and the group it is linked to,
    that way it's easier to check since user and hashtag must have the same group
    
    so need to fetch account table to link handle to group and fetch hashtag table to link hashtag to group, check if hashtag group
    is the same as account group and only then store it?
    yeah, that's what I thought
    '''
    
    
    #retrieve handle of tweet
    handle = '@' + str(status['user']['screen_name'])
    
    #retrieve its group(s can have multiple)
    accounts = []
    accounts = account.objects.filter(account_handle=handle)# just fetch the handle, can add a filter instead of for loop
    groups = []
    for acc in accounts:
        if acc.account_handle == handle: # selection of handles done in filter
            groups.append(acc.account_group)
    
    #retrieve hashtags associated with group
    hashtaglist = []
    hashtaglist = hashtag.objects.filter(hashtag_group__in = groups) # again can just use filter(hashtag_group__in =)
    for hasht in hashtaglist:
        for group in groups:
            if hasht.hashtag_group == group:
                
                #missing part, check if hashtag is in tweet...
                if str(hasht) in str(status['text']):
                    print 'new post'
#                
# #               
                    new_entry = tweet()
                    new_entry.tweet_id = status['id']
                    new_entry.tweet_handle = '@' + str(status['user']['screen_name'])
                    new_entry.tweet_text = status['text']
                    twitterdate_string = status['created_at']
                    #convert twittertime to djangotime
                    new_entry.tweet_created = parser.parse(twitterdate_string)
                    #call oembed to create a html of the tweet to store
                    new_entry.tweet_html = embed_tweet(new_entry.tweet_id, status['user']['screen_name'])
                    new_entry.save()
    
#    new_entry = tweet()
#    new_entry.tweet_id = status['id']
#    new_entry.tweet_handle = '@' + str(status['user']['screen_name'])
#    new_entry.tweet_text = status['text']
#    twitterdate_string = status['created_at']
#    #convert twittertime to djangotime
#    new_entry.tweet_created = parser.parse(twitterdate_string)
#    #call oembed to create a html of the tweet to store
#    new_entry.tweet_html = embed_tweet(new_entry.tweet_id, status['user']['screen_name'])
#    new_entry.save()

# listener Class Override
class listener(tweepy.StreamListener):
    
    def on_data(self, data):    
    # Twitter returns data in JSON format - we need to decode it first
        decoded = json.loads(data)
        #print decoded
        store_tweet(decoded)
        return True
        
    def on_error(self, status):
        print status
        if status == 420:
            return False

def stream_api():
    
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth)
    
    l = listener()
    stream = tweepy.Stream(auth = api.auth, listener=l)
    #only 1 stream per authentication, else 420 error
    try:
    
        handlelistx = []
        handlelistx = account.objects.all()
        #track_handlelist = [str(x.account_handle) for x in handlelistx ]
        follow_handlelist = [str(api.get_user(screen_name = str(x.account_handle)[1:]).id) for x in handlelistx ]
        print follow_handlelist
        #print "tracking"
        #user = api.get_user(screen_name = 'WuWaikai')
        #user2 = api.get_user(screen_name = 'Every3Minutes')
        #user3 = api.get_user(screen_name = 'notiven')
        #print user.id
        #stream.filter(track = str(track_handlelist))0
        stream.filter(follow = follow_handlelist)
        #stream.filter(follow = [str(user.id), str(user2.id), str(user3.id)], async=True)
        #print "done setting up track"
    except:
        print "well you fucked it"

#get handle objects

def search_api():
    #establishing connection to twitter REST API
    oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
    twitter = Twitter(auth=oauth)
    #try except, because if account table is empty, we don't search
    try:
        handlelist = []
        handlelist = account.objects.all()
        
        #get twitter results using handle objects
        # Search queries to be parsed by Twitter API
        result_list = []
        for handle in handlelist: # create a search for each handle
            searchq = 'from:' + handle.account_handle
            #temp_posts = twitter.search.tweets(q='from:@hm_morgan', result_type='recent', lang='en', count=4) # fix incase handlelist is empty
            temp_posts = twitter.search.tweets(q=searchq, result_type='recent', lang='en', count=10)
            result_list.append(temp_posts)
    except:
        pass
    
    for query_result in result_list: #iterate over each search query
        for n in range(len(query_result['statuses'])): #iterate over each status(tweet) in query and apply store function
            store_tweet(query_result['statuses'][n])

#launch separate threads fro search and stream
search_thread = Thread(target=search_api)
stream_thread = Thread(target=stream_api)

'''
need to consider that whenever new account has been added we need to restart the stream
also need manual restart button in case you want the new account's tweets

maybe add while statement which periodically checks if previous list used to start stream
is the same as the current list, if not then restart thread
----
must keep in mind the api limitations, so cant be restarting the stream every 10 seconds, more like 10 minutes,
but then also keep in mind if someone just changes the handle of someone rather than add/remove a handle, cant simply keep count

why not do it so that in models if something is saved it sets a global var changed to true then just check that and set it back
to false if stream has been restarted, so do it when the handle is assigned in the models
----
true, maybe check value has been changed, think there is a function
only on SAVED is not the best either I think, if you change the name but not handle, but something similar sounds good, yeah

The has_changed() method is used to determine if the field value has changed from the initial value. Returns True or False.
'''

search_thread.start()

'''
initial_count = changes whenever the stream starts?
updated_count = checks periodically and if this is diff then restart thread?

initial_count = account.objects.all().count()

def changed():
    global initial_count
    updated_count = account.objects.all().count()
    print initial_count
    print updated_count
    if initial_count != updated_count:
        print "change detected"
        stream_thread.join() #exit/stop doesn't exist
        stream_thread.start()
        initial_count = updated_count
    threading.Timer(10, changed).start() #checks if account table has been changed every 10 sec and only restarts when it is detected
'''

stream_thread.start()
#changed()