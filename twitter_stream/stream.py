try:
         import json
except ImportError:
        import simplejson as json

        
from .models import tweet
from .models import account
from twitter import Twitter, OAuth, TwitterHTTPError,TwitterStream


# Variables that contains the user credentials to access Twitter API

ACCESS_TOKEN = '235228993-UMgntnuS8UKyGU7pitxvMNxQO4Eqte2tgAGk9ijK'
ACCESS_SECRET = '9I8YOVtb6zIZaPpQEnAdVOZaq6vNBZJZVaRiU2OZir8os'
CONSUMER_KEY = 'pPa5GLuxOLzK57woQ1pdYQIAf'
CONSUMER_SECRET = 'IAsBqLL6lOQdcZ4VRu1ZIPvTOMIDw2Pa4bMbPtXbxP8Xwkjjd6'

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)



twitter = Twitter(auth=oauth)

# Search queries to be parsed by Twitter API

#get handle objects
handlelist = ["one_item"]
handlelist = account.objects.all()

#get twitter results using handle objects

result_list = []
for handle in handlelist: # create a search for each handle
    searchq = 'from:' + handle.account_handle
    #temp_posts = twitter.search.tweets(q='from:@hm_morgan', result_type='recent', lang='en', count=4) # fix incase handlelist is empty
    temp_posts = twitter.search.tweets(q=searchq, result_type='recent', lang='en', count=10)
    result_list.append(temp_posts)
    

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
        new_entry.tweet_handle = query_result['statuses'][n]['user']['screen_name']
        new_entry.tweet_text = query_result['statuses'][n]['text']
        new_entry.tweet_profile_picture = query_result['statuses'][n]['user']['profile_image_url_https']
        #twitterdate_string = str(query_result['statuses'][n]['created_at'])
        #print twitterdate_string
        #twitterdate = twitterdate_string.split()
        #djangodate = '' + str(datetime.date.today().year) +'-'+ str(strptime(twitterdate[1],'%b').tm_mon) +'-'+ twitterdate[2] +' '+ twitterdate[3]
        #print djangodate
        #new_entry.tweet_created = "2017-2-09 10:26:16"
        new_entry.tweet_created = query_result['statuses'][n]['created_at'] #<<<<<< Convert to date timel
        #'%Y-%m-%d %H:%M:%S',     # '2006-10-25 14:30:59' is the syntax of datetimefield, but twitter returns
    #               "created_at":"Wed Aug 27 13:08:45 +0000 2008"
        #new_entry.tweet_expand_url = query_result['statuses'][n]['entities']['media'][0]['url']
        
        try:
            new_entry.tweet_expand_url = query_result['statuses'][n]['entities']['media'][0]['expanded_url']
            new_entry.tweet_image = query_result['statuses'][n]['entities']['media'][0]['media_url']
        except:
            new_entry.tweet_expand_url = ""
            new_entry.tweet_image = ""
        new_entry.save()