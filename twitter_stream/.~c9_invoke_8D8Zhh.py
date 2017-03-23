from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import Context, loader
from .models import tweet, group, account
import datetime
import twitter_stream
import stream
import json

# Create your views here.

# returns a tuple of a list of tweets, the groups used and how many pinned tweets there are
# , given the group. 
def get_group_tweets(tgroup_name):
    all_groups = group.objects.all()    #checks to find group
    all_group_names = []
    group_found = False
    target_group = group()
    for g_name in all_groups:
        all_group_names.append(str(g_name.group_name))
        if str(g_name.group_name) == tgroup_name:
            group_found = True  #found group
            target_group = g_name
    if group_found == False:
        template = loader.get_template('noGroupFound.html')
        #response if there was no such group
        context = Context({"available_groups": all_group_names})
        return HttpResponse(template.render(context))
    

    #find all subgroups of given group
    num_of_groups = 0
    list_of_groups = []
    list_of_groups.append(target_group)
    level = target_group.group_level + 1
    while len(list_of_groups) > num_of_groups: # 
        num_of_groups = len(list_of_groups)
        for group_object in [x for x in all_groups if x.group_level==level]:# iterates over each group in given list
            if str(group_object.group_parent) in list_of_groups:# could do more optimisation using sub lists for each level
                list_of_groups.append(group_object.group_name)
        level += 1
        
    #need to find all handles belonging to our list_of_groups
    list_of_accounts = account.objects.filter(account_group__in=list_of_groups)
    list_of_handles = []
    print list_of_accounts
    for acc in list_of_accounts:
        list_of_handles.append(acc.account_handle)

    
    #need to change all tweets to only tweets associated with the handles in the last step
   
    tweets = tweet.objects.filter(tweet_handle__in=list_of_handles)# need to order tweets by datetime
    tweets = tweets.order_by('-tweet_created')
    # put pinned tweets to front and make tweet dark themed
    pinned_tweets = []
    norm_tweets = []
    for t in tweets:
        if  t.tweet_pin == tgroup_name:
            pinned_tweets.append(t)
        else:
            norm_tweets.append(t)
            
    tot_tweets = []
    for t in pinned_tweets: # brings all tweets together again, but with pinned ones at the start
        tot_tweets.append(t)
    for t in norm_tweets:
        tot_tweets.append(t)
    tweet_data = (tot_tweets, all_group_names, len(pinned_tweets))
    return tweet_data

# Display the received tweets

def index(request, tgroup_name=''): #second param "group"
    tweet_data = get_group_tweets(tgroup_name)
    tot_tweets = tweet_data[0]
    all_group_names = tweet_data[1]
    num_of_pins = tweet_data[2]
        
    # Define arrays
    tweet_text = []
    tweet_html = []
    
    # Iterate through the tweets
    
    for n in range(min(len(tot_tweets),50)): # displaying more than 200 tweets does not display properly
        tweet_html.append(tot_tweets[n].tweet_html)
        tweet_text.append(tot_tweets[n].tweet_text)
        
    template = loader.get_template('index.html')
    groupnamewithoutunderscore = tgroup_name.replace("_", " ")
# range in context is used for iterating over each tweet
   
    context = Context({"embedhtml":tweet_html, "tweet": tweet_text, "four": range(4), "range": range(len(tweet_text)), "groups": groupnamewithoutunderscore, "available_groups": all_group_names, "pin_count": num_of_pins})

       
    return HttpResponse(template.render(context))
    
def home(request):
    all_groups = group.objects.all()
    context = Context({"available_groups": all_groups})   
   
    template = loader.get_template('home.html')  # if nothing in q then just load home 
 
        
    return HttpResponse(template.render(context))
    
    
def search(request, group, search_string):
    #retrieve tweets from db
    tweet_data = get_group_tweets(group)
    tweets = tweet_data[0]
    all_group_names = tweet_data[1]
    num_of_pins = tweet_data[2]
    
    #do the search bit
    for t in tweets:
        i
    
    
    #return the page to the user
    context = Context({}) # this would probably look simmilar to the context from the index.html
    template = loader.get_template('search.html')
    
    return HttpResponse(template.render(context))
    
    
