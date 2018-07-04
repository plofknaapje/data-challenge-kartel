# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 22:23:44 2018

@author: Vincent_Vast
"""

import re
import seaborn as sns; sns.set()
import pandas as pd
import seaborn as sns; sns.set()
import operator

 
# Create a function to make all the letters lowercase and remove extra non-letter symbols.
regex = re.compile('[^a-zA-z ]')
# Read the CSV file
df_AA = pd.read_csv('sentiment_AA.csv')
# Filter the dataframe on tweets that are classified as negative tweets.
# If you want positive tweets change the filter.
df_AA_filter = df_AA[df_AA['sentiment'] <= -0.33]
filter_lst = []
for i in df_AA_filter['text']:
    # Filter all the tweets in the dataframe from upper to lowercase symbols and other non letter symbols.
    tweet = regex.sub('', i)
    filter_lst.append(tweet)
df_count = pd.DataFrame()
df_count['text'] = 0
df_count['text'] = filter_lst
df_count.head()
counted_dict_sentiment = {}
# Count the words that are with negative sentiment.
def word_count(string):
    my_string = string.lower().split()
    for item in my_string:
        if item in counted_dict_sentiment:
            counted_dict_sentiment[item] += 1
        else:
            counted_dict_sentiment[item] = 1
 
for i in df_count['text']:
    word_count(i)

# Now do the same for all the words that appear in the tweets to AA
# without filtering on sentiment.
df_AA.head()
AA_lst = []
for i in df_AA['text']:
    tweet = regex.sub('', i)
    AA_lst.append(tweet)
df_count_AA = pd.DataFrame()
df_count_AA['text'] = 0
df_count_AA['text'] = AA_lst
df_count_AA.head()
counted_dict_all = {}
def word_count(string):
    my_string = string.lower().split()
    for item in my_string:
        if item in counted_dict_all:
            counted_dict_all[item] += 1
        else:
            counted_dict_all[item] = 1
           
for i in df_count_AA['text']:
    word_count(i)

fin_dict = {}

for key in counted_dict_sentiment.keys():
    if counted_dict_sentiment[key] > 1000:
        if key in counted_dict_sentiment:
            fin_dict[key] = counted_dict_sentiment[key]/counted_dict_all[key]

# Get the ratio of total words against the words that have positive/negative sentiment. 
# Only do this for the words that appear more than 1000 times so that
# words that do not appear so often get filtered out. 
sorted_fin = sorted(fin_dict.items(), key=operator.itemgetter(1))

# Print final dictionary/put it in dataframe.
print(sorted_fin)
pd.DataFrame(sorted_fin[:-100])