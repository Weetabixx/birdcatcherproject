import datetime
import twitter_stream
import stream
import json

from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import Context
from django.template import loader
from .forms import searchform
from middleware import browserDetection
from django.shortcuts import redirect
from .models import tweet
from .models import group
from .models import account

# Create your views here.

# returns a tuple of a list of tweets, the groups used and how many pinned
# tweets there are, given the group. or returns a redirect to a no group found. 
def get_group_tweets(tgroup_name):
    
    #grabs all groups
    all_groups = group.objects.all()
    all_group_names = []
    group_found = False
    
    #creates a instance of a group
    target_group = group()
    for g_name in all_groups:
        all_group_names.append(str(g_name.group_name))
        if str(g_name.group_name) == tgroup_name:
            
            #found group
            group_found = True
            target_group = g_name
    if group_found == False:
        template = loader.get_template('noGroupFound.html')
        
        #redirect response if there was no such group
        return redirect("/noGroupFound")
    
    #find all subgroups of given group
    num_of_groups = 0
    list_of_groups = []
    list_of_groups.append(target_group)
    level = target_group.group_level + 1
    while len(list_of_groups) > num_of_groups: # 
        num_of_groups = len(list_of_groups)
       
        # iterates over each group per level to see if it
        for group_object in [x for x in all_groups if x.group_level==level]:
            
            # is a child that should have its tweets displayed
            if str(group_object.group_parent) in list_of_groups:                
                list_of_groups.append(group_object.group_name)
        level += 1
        
    #need to find all handles belonging to our list_of_groups
    list_of_accounts = account.objects.filter(account_group__in=list_of_groups)
    list_of_handles = []
    print list_of_accounts
    for acc in list_of_accounts:
        list_of_handles.append(acc.account_handle)

    #need to find all tweets associated with our list_of_handles
    #and need to order tweets by datetime
    tweets = tweet.objects.filter(tweet_handle__in=list_of_handles)
    tweets = tweets.order_by('-tweet_created')
    
    # seperate pinned tweets from normal tweets
    pinned_tweets = []
    norm_tweets = []
    for t in tweets:
        if  t.tweet_pin == tgroup_name:
            pinned_tweets.append(t)
        else:
            norm_tweets.append(t)
            
    # brings all tweets together again, but with pinned ones at the start        
    tot_tweets = []
    for t in pinned_tweets:
        tot_tweets.append(t)
    for t in norm_tweets:
        tot_tweets.append(t)
    
    # removes the script of the embedded tweets
    for t in tot_tweets:    
        t.tweet_html = t.tweet_html.split("<script>")[0]
        
    #brings tweets and information about the tweets together and returns it
    tweet_data = (tot_tweets, all_group_names, len(pinned_tweets),)
    return tweet_data
    

# if no group, re-go to nogroupfound.html
def noGroup(request):
    template = loader.get_template('noGroupFound.html')
    all_groups = group.objects.all()
    all_group_names = []
    for g_name in all_groups:
        all_group_names.append(str(g_name.group_name))
    context = Context({"available_groups": all_group_names})
    return HttpResponse(template.render(context))
    

# Display the received tweets
#second param "tgroup_name" implies which group to display
def index(request, tgroup_name=''):
    
    # retrieve tweets associated with the target group
    # if no group was found return the no group found page
    tweet_data = get_group_tweets(tgroup_name)
    if type(tweet_data) is HttpResponseRedirect:
        return tweet_data
    tot_tweets = tweet_data[0]
    all_group_names = tweet_data[1]
    num_of_pins = tweet_data[2]
        
    # Define arrays to be used for context
    tweet_text = []
    tweet_html = []
    
    # Iterate through the tweets
    # displaying more than 200 tweets does not display properly and more than 
    # 30 slows down the rendering of the tweets
    for n in range(min(len(tot_tweets),30)):
        tweet_html.append(tot_tweets[n].tweet_html)
        tweet_text.append(tot_tweets[n].tweet_text)

    template = loader.get_template('index.html')
    groupnamewithoutunderscore = tgroup_name.replace("_", " ")

    #create form for search
    form = searchform()
    
    # range in context is used for iterating over each tweet
    context = Context({"embedhtml":tweet_html, 
                       "tweet": tweet_text, 
                       "range": range(len(tweet_text)), 
                       "groups": groupnamewithoutunderscore, 
                       "group_name": tgroup_name, 
                       "available_groups": all_group_names, 
                       "pin_count": num_of_pins, "form": form})

       
    return HttpResponse(template.render(context))
    
def home(request):
    all_groups = group.objects.all()
    
    context = Context({"available_groups": all_groups})   

    template = loader.get_template('home.html')
 
    return HttpResponse(template.render(context))
    
    
def search(request, group='', search_string=''):
    if request.method == 'GET':
        # create a form instance and populate it with data from the request:
        form = searchform(request.GET)
        if form.is_valid():
        
            # process the data in form.cleaned_data as required
            group = form.cleaned_data['group']
            search_string = form.cleaned_data['search_string']
            print group
            print search_string
            
            #retrieve tweets from db
            tweet_data = get_group_tweets(group)
            if type(tweet_data) is HttpResponseRedirect:
                return tweet_data
            tweets = tweet_data[0]
            all_group_names = tweet_data[1]
            num_of_pins = tweet_data[2]
            groupnamewithoutunderscore = group.replace("_", " ")
            tweet_text = []
            tweet_html = []
            
            #do the search bit
            for t in tweets:
                if len(tweet_text) < 200: # displaying more than 200 tweets does not display properly
                    if search_string in t.tweet_handle:
                        tweet_text.append(t.tweet_text)
                        tweet_html.append(t.tweet_html)
                    elif search_string in t.tweet_text:
                        tweet_text.append(t.tweet_text)
                        tweet_html.append(t.tweet_html)
            
            #return the page to the user
    
            context = Context({"embedhtml":tweet_html, 
                               "tweet": tweet_text, 
                               "range": range(len(tweet_text)), 
                               "groups": groupnamewithoutunderscore, 
                               "group_name": group, 
                               "available_groups": all_group_names,
                               "form": form}) 

            template = loader.get_template('index.html')
            
            return HttpResponse(template.render(context))
            
        else:
            try:    #try to return to the group page, else go to home
                return HttpResponseRedirect('/' + form.cleaned_data['group'])
            except:
                return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')
