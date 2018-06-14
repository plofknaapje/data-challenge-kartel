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
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyser = SentimentIntensityAnalyzer()

regex = re.compile('[^a-zA-z ]')
df_AA = pd.read_csv('sentiment_AA.csv')
df_AA_filter = df_AA[df_AA['sentiment'] <= -0.5]
filter_lst = []
for i in df_AA_filter['text']:
    tweet = regex.sub('', i)
    filter_lst.append(tweet)
df_count = pd.DataFrame()
df_count['text'] = 0
df_count['text'] = filter_lst
df_count.head()
my_dict = {}
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

sorted_x = sorted(my_dict.items(), key=operator.itemgetter(1))
twan = (sorted_x.reverse())
print(twan)
print(sorted_x)
