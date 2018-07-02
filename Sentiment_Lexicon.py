# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 22:23:44 2018

@author: Vincent_Vast
"""
 
import access
from textblob import TextBlob
import re
import pickle
from datetime import datetime, timedelta
import seaborn as sns; sns.set()
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
import numpy as np
#from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
#analyser = SentimentIntensityAnalyzer()
 
#Create a function to make all the letters lowercase and remove extra non-letter symbols.
regex = re.compile('[^a-zA-z ]')
#Read the CSV file
df_AA = pd.read_csv('sentiment_AA.csv')
#Filter the dataframe on tweets that are classified as positive tweets.
#If you want negative tweets change the filter.
df_AA_filter = df_AA[df_AA['sentiment'] <= 0.33]
filter_lst = []
for i in df_AA_filter['text']:
    #Filter all the tweets in the dataframe from upper to lowercase symbols and other non letter symbols
    tweet = regex.sub('', i)
    filter_lst.append(tweet)
df_count = pd.DataFrame()
df_count['text'] = 0
df_count['text'] = filter_lst
df_count.head()
my_dict = {}
#Count the words that are with positive sentiment
def word_count(string):
    my_string = string.lower().split()
    for item in my_string:
        if item in my_dict:
            my_dict[item] += 1
        else:
            my_dict[item] = 1
 
 
for i in df_count['text']:
    word_count(i)
 
print(my_dict)
import operator
#Sort all the words on the number of times the word appears.
sorted_x = sorted(my_dict.items(), key=operator.itemgetter(1))
sorted_x_reversed = (sorted_x.reverse())
print(sorted_x_reversed)
print(sorted_x)
 
#Now do the same for all the words that appear in the tweets to AA
#Without filtering on sentiment. 
df_AA.head()
AA_lst = []
for i in df_AA['text']:
    tweet = regex.sub('', i)
    AA_lst.append(tweet)
df_count_AA = pd.DataFrame()
df_count_AA['text'] = 0
df_count_AA['text'] = AA_lst
df_count_AA.head()
my_dict_AA = {}
def word_count(string):
    my_string = string.lower().split()
    for item in my_string:
        if item in my_dict_AA:
            my_dict_AA[item] += 1
        else:
            my_dict_AA[item] = 1
           
 
 
 
for i in df_count_AA['text']:
    word_count(i)
 
print(my_dict_AA)
import operator
 
sorted_x_AA = sorted(my_dict_AA.items(), key=operator.itemgetter(1))
twan_AA = (sorted_x_AA.reverse())
print(twan_AA)
print(sorted_x_AA)
fin_dict = {}

for key in my_dict.keys():
    if my_dict[key] > 1000:
        if key in my_dict:
            fin_dict[key] = my_dict[key]/my_dict_AA[key]
#Get the ratio of total words against the words that have positive/negative sentiment. 
#Only do this for the words that appear more than 1000 times so that
#Words that do not appear so often get filtered out.
print(fin_dict)
 
sorted_fin = sorted(fin_dict.items(), key=operator.itemgetter(1))
#Print final dictionary/put it in dataframe.
print(sorted_fin)
pd.DataFrame(sorted_fin[:-100])