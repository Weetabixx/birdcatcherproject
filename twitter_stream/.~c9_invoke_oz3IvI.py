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

def embed_tweet(tweet_id,tweet_handle):
    response = consumer.embed("https://twitter.com/"+tweet_handle+"/status/" + str(tweet_id))
    html_tweet = response["html"]
    return html_tweet

# Search queries to be parsed by Twitter API

#get handle objects

#get twitter results using handle objects
try:
    handlelist = ["one_item"]
    handlelist = account.objects.all()
    
    result_list = []
    for handle in handlelist: # create a search for each handle
        searchq = 'from:' + handle.account_handle
        #temp_posts = twitter.search.tweets(q='from:@hm_morgan', result_type='recent', lang='en', count=4) # fix incase handlelist is empty
        temp_posts = twitter.search.tweets(q=searchq, result_type='recent', lang='en', count=10, -f)
        result_list.append(temp_posts)
    print "completed search"
except:
    pass

# Open or create text file

#text_file = open("twitter_stream_1000tweets.json", "w")

# Write the json dump to this text file

#text_file.write(json.dumps(recent_posts))

# Close file

#text_file.close()

# Place tweets in Database(to be completed)
for query_result in result_list: # iterate over each search query
    for n in range(len(query_result['statuses'])): # iterate over each status in query
        new_entry = tweet()
        new_entry.tweet_id = query_result['statuses'][n]['id']
        new_entry.tweet_handle = '@' + str(query_result['statuses'][n]['user']['screen_name'])
        new_entry.tweet_text = query_result['statuses'][n]['text']
        #new_entry.tweet_profile_picture = query_result['statuses'][n]['user']['profile_image_url_https']
        twitterdate_string = query_result['statuses'][n]['created_at']
        #twitterdate_string = time.strftime('%Y-%m-%d %H:%M:%S +0000', time.strptime(query_result['statuses'][n]['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
        #twitterdate_string = datetime.strptime(twitterdate_string,'%a %b %d %H:%M:%S %z %Y');
        #print twitterdate_string
        #print twitterdate_string
        #twitterdate = twitterdate_string.split()
        #djangodate = '' + str(datetime.date.today().year) +'-'+ str(strptime(twitterdate[1],'%b').tm_mon) +'-'+ twitterdate[2] +' '+ twitterdate[3]
        #print djangodate
        #new_entry.tweet_created = "2017-02-09 10:26:16"
        #new_entry.tweet_created = query_result['statuses'][n]['created_at'] #<<<<<< Convert to date timel
        twi
        new_entry.tweet_created = parser.parse(twitterdate_string)
        
        #'%Y-%m-%d %H:%M:%S',     # '2006-10-25 14:30:59' is the syntax of datetimefield, but twitter returns
        #               "created_at":"Wed Aug 27 13:08:45 +0000 2008"
        #new_entry.tweet_expand_url = query_result['statuses'][n]['entities']['media'][0]['url']
        
        #call oembed to create a html of the tweet to store
        new_entry.tweet_html = embed_tweet(new_entry.tweet_id, query_result['statuses'][n]['user']['screen_name'])
        
        new_entry.save()
        
        
        
    # need to create repeating steam here but not to keep steam.py running because it would hold up the server