
# coding: utf-8

# In[6]:

# Twitter features by ChangQing Wang        
# Feature 2, check average degree of hashtags within last 60 sec    

import json # For parsing json code
from collections import defaultdict # Set default value for dictionaries
import dateutil.parser # Parsing timestamp

# For feature 1, check the given string, return 1 if non_ascii exists, 0 otherwise
def remove_non_ascii(text):
    flag = 0
    res = ""
    for i in text:
        if ord(i) < 32 or ord(i) > 127:
            flag = 1
            if (i == "\n" or i == "\t"):
                res = res + " "
            if (i == "\'"):
                res = res + "'"   
            if (i == "\""):
                res = res + '"'  
            if (i == "\\\\"):
                res = res + '\\'
            if (i == "\/"):
                res = res + "/"
        else: 
            res = res + i
    return flag, res         

# For the realization of feature 2, extract all unique hashtags from given string
def extract_hash_tags(str):
    return set(s[1:].lower() for s in str.split() if s.startswith('#'))

outfile2 = open('./tweet_output/ft2.txt', 'w')
Hashtagdegree = {} # Save the degree of the hashtags
Hashtagdegree = defaultdict(lambda: 0, Hashtagdegree)
Hashtagreserves = {} # Hashtag dicts with timestamp as keys 
timeseries = []
Avgdegree = 0
time_range = 60

with open('./tweet_input/tweets.txt') as myfile:
    count  = 0
    for line in myfile:
    #for line in reversed(myfile.readlines()): # to use if tweet.txt is in reversed time order 
        # Feature 1, write "clean" tweets
        json_parsed = json.loads(line)
        flag, cleantweet = remove_non_ascii(json_parsed['text'])
        time = json_parsed['created_at']        
        time_parsed = dateutil.parser.parse(time, fuzzy = True)
        timeseries.append(time_parsed)
        hashtags = extract_hash_tags(cleantweet.encode('ascii','ignore'))
        
        for t in timeseries:
            time_delta = time_parsed - t
            if time_delta.seconds <= time_range:
                break
            timeseries.remove(t)
            if t in Hashtagreserves:
                dict_to_remove = Hashtagreserves[t]
                for htag, htag_val in dict_to_remove.iteritems():
                    Hashtagdegree[htag] = Hashtagdegree[htag] - htag_val
                    if Hashtagdegree[htag] == 0:
                        del Hashtagdegree[htag]
                del Hashtagreserves[t]
            
        
        Num = len(hashtags)       
        if Num > 1: # if more than one hashtag, update and average hashtag degrees
            dict_temp = {}
            for i in hashtags:
                dict_temp[i] = Num - 1
                Hashtagdegree[i] = Hashtagdegree[i] + (Num - 1)  
            Hashtagreserves[time_parsed] = dict_temp    
            Avgdegree = sum(Hashtagdegree.values()) / float(len(Hashtagdegree)) 

        outfile2.write("%0.2f" % Avgdegree)
        outfile2.write('\n')

outfile2.close()    


# In[ ]:



