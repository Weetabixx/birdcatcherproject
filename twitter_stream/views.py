from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, loader
from .models import tweet
import datetime
import twitter_stream
import stream
import json
import oembed


# Create your views here.

# Display the received tweets

def index(request):
  #  try:
  #      import json
  #  except ImportError:
  #      import simplejson as json
        
    # Open the json file for reading 
    
   # with open('twitter_stream_1000tweets.json') as json_file:  
        
    # Assign the json data to variable tweet
   
    tweets = tweet.objects.all()
    
    # Define arrays
    tweet_text = []
    #tweet_profile_picture = []
    #tweet_expand_url = []
    #tweet_image = []
    tweet_html = []
    
    consumer = oembed.OEmbedConsumer()
    endpoint = oembed.OEmbedEndpoint('https://publish.twitter.com/oembed?', 'https://twitter.com/*' )
    consumer.addEndpoint(endpoint)
    # need to move oembed to steam.py
    
    # Iterate through the tweets
    
    for n in range(len(tweets)):
        tweet_html.append(tweets[n].tweet_html)
        tweet_text.append(tweets[n].tweet_text)
        
        
    template = loader.get_template('index.html')

# range in context is used for iterating over each tweet

    context = Context({"embedhtml":tweet_html, "tweet": tweet_text, "four": range(4), "range": range(len(tweet_text))})


    return HttpResponse(template.render(context))