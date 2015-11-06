
# coding: utf-8

# In[5]:

# Twitter features by ChangQing Wang
import json # For parsing json code

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

outfile = open('./tweet_output/ft1.txt', 'w')

with open('./tweet_input/tweets.txt') as myfile:
    count  = 0
    for line in myfile:
    #for line in reversed(myfile.readlines()): # to use if tweet.txt is in reversed time order 
        # Feature 1, write "clean" tweets
        json_parsed = json.loads(line)
        flag, cleantweet = remove_non_ascii(json_parsed['text'])
        time = json_parsed['created_at']
        count = count + flag
        outfile.write(cleantweet + " (timestamp: "+ time + ")") 
        outfile.write('\n')

if count > 1:
    s = repr(count) + ' tweets contained unicode.'
else:
    s = repr(count) + ' tweet contained unicode.'
outfile.write(s) 
outfile.close()

