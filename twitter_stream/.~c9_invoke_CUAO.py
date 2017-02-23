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


# Variables that contains the user credentials to access Twitter API

ACCESS_TOKEN = '235228993-UMgntnuS8UKyGU7pitxvMNxQO4Eqte2tgAGk9ijK'
ACCESS_SECRET = '9I8YOVtb6zIZaPpQEnAdVOZaq6vNBZJZVaRiU2OZir8os'
CONSUMER_KEY = 'pPa5GLuxOLzK57woQ1pdYQIAf'
CONSUMER_SECRET = 'IAsBqLL6lOQdcZ4VRu1ZIPvTOMIDw2Pa4bMbPtXbxP8Xwkjjd6'


oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

twitter = Twitter(auth=oauth)

consumer = oembed.OEmbedConsumer()
endpoint = oembed.OEmbedEndpoint('https://publish.twitter.com/oembed?', 'https://twitter.com/*' )
consumer.addEndpoint(endpoint)
#functio
#function to retrieve embedded tweet
def embed_tweet(tweet_id,tweet_handle):
    response = consumer.embed("https://twitter.com/"+tweet_handle+"/status/" + str(tweet_id))
    html_tweet = response["html"]
    return html_tweet
    
def store_tweet(status): # stores a status in the database and retrieves a embeded html code
    new_entry = tweet()
    new_entry.tweet_id = status['id']
    new_entry.tweet_handle = '@' + str(status['user']['screen_name'])
    new_entry.tweet_text = status['text']
    twitterdate_string = status['created_at']
    new_entry.tweet_created = parser.parse(twitterdate_string)#convert twittertime to djangotime
    #call oembed to create a html of the tweet to store
    new_entry.tweet_html = embed_tweet(new_entry.tweet_id, status['user']['screen_name'])
    
    new_entry.save()

# Search queries to be parsed by Twitter API

#launch thread to gather tweets continuously

# listener Class Override

start_time = time.time() #grabs the system time

class listener(StreamListener):
        
    def on_data(self, data):    
	# Twitter returns data in JSON format - we need to decode it first
        decoded = json.loads(data)
        store_tweet(decoded)
 
	def on_error(self, status):
	    pass
		#print statuses
		
l = listener()
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

stream = Stream(auth, l)

stream.filter(track=['programming'])


#get handle objects



try:
    handlelist = ["one_item"]
    handlelist = account.objects.all()
    
    result_list = []
    for handle in handlelist: # create a search for each handle
        searchq = 'from:' + handle.account_handle
        #temp_posts = twitter.search.tweets(q='from:@hm_morgan', result_type='recent', lang='en', count=4) # fix incase handlelist is empty
        temp_posts = twitter.search.tweets(q=searchq, result_type='recent', lang='en', count=10)
        result_list.append(temp_posts)
    print "completed search"
except:
    pass


# Place tweets in Database
for query_result in result_list: # iterate over each search query
    for n in range(len(query_result['statuses'])): # iterate over each status in query
        store_tweet(query_result['statuses'][n])
    
    

        
        
        
    # need to create repeating steam here but not to keep steam.py running because it would hold up the server