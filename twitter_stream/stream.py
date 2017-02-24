# -*- coding: utf-8 -*-

try:
         import json
except ImportError:
        import simplejson as json

        
from .models import tweet
from .models import account
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

# listener Class Override
class listener(tweepy.StreamListener):
    
    def on_data(self, data):    
    # Twitter returns data in JSON format - we need to decode it first
        decoded = json.loads(data)
        print decoded
        store_tweet(decoded)
        return True
        
    def on_error(self, status):
        print status
        if status == 420:
            return False

def stream_api():
    
    l = listener()
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth)
    
    stream = Stream(auth, l)
    #only 1 stream per authentication, else 420 error
    try:
    
        handlelistx = []
        handlelistx = account.objects.all()
        track_handlelist = [str(x.account_handle) for x in handlelistx ]
        print track_handlelist
        print "tracking"
        user = api.get_user(screen_name = 'WuWaikai')
        print user.id
        #stream.filter(track = str(track_handlelist))0
        stream.filter(follow = [str(user.id)], async=True)
        print "done setting up track"
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
search_thread.start()
#stream_thread.start()
