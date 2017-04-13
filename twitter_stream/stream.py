# -*- coding: utf-8 -*-

try:
         import json
except ImportError:
        import simplejson as json
        
import tweepy
import oembed
import time
import os
import threading
import requests.packages.urllib3
import requests

from datetime import datetime
from dateutil import parser
from django.db import transaction
from .models import tweet
from .models import account
from .models import hashtag
from threading import Thread
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from twitter import Twitter
from twitter import OAuth
from twitter import TwitterHTTPError
from twitter import TwitterStream


# Variables that contains the user credentials to access Twitter API
ACCESS_TOKEN = '235228993-UMgntnuS8UKyGU7pitxvMNxQO4Eqte2tgAGk9ijK'
ACCESS_SECRET = '9I8YOVtb6zIZaPpQEnAdVOZaq6vNBZJZVaRiU2OZir8os'
CONSUMER_KEY = 'pPa5GLuxOLzK57woQ1pdYQIAf'
CONSUMER_SECRET = 'IAsBqLL6lOQdcZ4VRu1ZIPvTOMIDw2Pa4bMbPtXbxP8Xwkjjd6'

#Establish connection to twitter for embedded tweet
consumer = oembed.OEmbedConsumer()
endpoint = oembed.OEmbedEndpoint('https://publish.twitter.com/oembed?', 
                                 'https://twitter.com/*' )
consumer.addEndpoint(endpoint)


#function to retrieve embedded tweet
def embed_tweet(tweet_id,tweet_handle):
    response = consumer.embed("https://twitter.com/"+tweet_handle+"/status/" 
                              + str(tweet_id))
    html_tweet = response["html"]
    return html_tweet


#stores a tweet in the database and retrieves an embedded html code
def save_status(status):
    new_entry = tweet()
    new_entry.tweet_id = status['id']
    new_entry.tweet_handle = '@' + str(status['user']['screen_name'])
    new_entry.tweet_text = status['text']
    twitterdate_string = status['created_at']
    #convert twittertime to djangotime
    new_entry.tweet_created = parser.parse(twitterdate_string)
    #call oembed to create a html of the tweet to store
    new_entry.tweet_html = embed_tweet(new_entry.tweet_id, status['user']
                                       ['screen_name'])
    new_entry.save()
    

def store_tweet(status):
    #retrieve handle of tweet
    handle = '@' + str(status['user']['screen_name'])
    
    #retrieve its group(s can have multiple)
    accounts = []
    
    # just fetch the handle, can add a filter instead of for loop
    accounts = account.objects.filter(account_handle=handle)
    groups = []
    for acc in accounts:
        if acc.filter_by_hashtags == False:
            save_status(status)
            return
        
        # selection of handles done in filter
        if acc.account_handle == handle: 
            groups.append(acc.account_group)
    
    #retrieve hashtags associated with group
    hashtaglist = []
    
    # again can just use filter(hashtag_group__in =)
    hashtaglist = hashtag.objects.filter(hashtag_group__in = groups)
    for hasht in hashtaglist:
        #remove emojis, because they return an error
        if hasht.hashtag_hash in status['text'].encode('ascii', 'ignore').decode('ascii'):
            print 'new post'
            save_status(status)


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
        follow_handlelist = [str(api.get_user(screen_name = str(x.account_handle)[1:]).id) for x in handlelistx ]
        stream.filter(follow = follow_handlelist)
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
            temp_posts = twitter.search.tweets(q=searchq, result_type='recent', 
                                               lang='en', count=1)
            result_list.append(temp_posts)
    except:
        pass
    
    #iterate over each search query
    for query_result in result_list:
        #iterate over each status(tweet) in query and apply store function
        for n in range(len(query_result['statuses'])):
            store_tweet(query_result['statuses'][n])


#launch separate threads fro search and stream
search_thread = Thread(target=search_api)
stream_thread = Thread(target=stream_api)

search_thread.start()
stream_thread.start()