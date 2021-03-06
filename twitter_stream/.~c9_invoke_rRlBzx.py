from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, loader
from .models import tweet, group, account
import datetime
import twitter_stream
import stream
import json


# Create your views here.

# Display the received tweets

print
def index(request, group_name=''): #second param "group" 

    all_groups = group.objects.all()    #checks to find group
    all_group_names = []
    group_found = False
    for g_name in all_groups:
        all_group_names.append(str(g_name.group_name))
        if str(g_name.group_name) == group_name:
            group_found = True  #found group
            target_group = g_name
    if group_found == False:
        template = loader.get_template('noGroupFound.html') #response if there was no such group
        context = Context({"available_groups": all_group_names})
        return HttpResponse(template.render(context))
    
    #find all subgroups of given group
    num_of_groups = 0
    list_of_groups = []
    list_of_groups.append(group_name)
    level = target_group.group_level + 1
    while len(list_of_groups) > num_of_groups: # 
        num_of_groups = len(list_of_groups)
        for group_object in [x for x in all_groups if x.group_level==level]:# iterates over each group in given list
            if group_object.group_parent in list_of_groups:# could do more optimisation using sub lists for each level
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
    # Define arrays
    tweet_text = []
    tweet_html = []
    
    # Iterate through the tweets
    
    for n in range(len(tweets)):
        tweet_html.append(tweets[n].tweet_html)
        tweet_text.append(tweets[n].tweet_text)
        
    template = loader.get_template('index.html')

# range in context is used for iterating over each tweet

    context = Context({"embedhtml":tweet_html, "tweet": tweet_text, "four": range(4), "range": range(len(tweet_text)), "groups": group_name})


    return HttpResponse(template.render(context))
    

print "views.py finished"