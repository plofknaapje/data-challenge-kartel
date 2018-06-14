

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
from textblob import TextBlob

database = access.db
conversationList = []

airlines_id = ["56377143", "106062176", "18332190", "22536055", "124476322", "26223583", "2182373406", "38676903",
               "1542862735", "253340062", "218730857", "45621423", "20626359"]
airlines_names = ["KLM", "AirFrance", "British_Airways", "AmericanAir", "Lufthansa", "AirBerlin", "AirBerlin assist",
                  "easyJet", "RyanAir", "SingaporeAir", "Qantas", "EtihadAirways", "VirginAtlantic"]
airlines_other_id = ["56377143", "106062176", "18332190", "124476322", "26223583", "2182373406", "38676903",
                     "1542862735", "253340062", "218730857", "45621423", "20626359"]
airlines_other_names = ["KLM", "AirFrance", "British_Airways", "Lufthansa", "AirBerlin", "AirBerlin assist", "easyJet",
                        "RyanAir", "SingaporeAir", "Qantas", "EtihadAirways", "VirginAtlantic"]
counterair = 0
dfairlines = pd.DataFrame()
for airline in airlines_names:
    dfprop = pd.DataFrame()
# Default for AA
    user_id = airlines_id[counterair]
    user_name = airlines_names[counterair]

 # VOOR SENTIMENT PAS VANAF HIR BELANGERIJK   
    
     
    def processTweet(tweet):
        # process the tweets
     
        #Convert to lower case
        tweet = tweet.lower()
        #Convert www.* or https?://* to URL
        tweet = re.sub('((www.[^\s]+)|(https?://[^\s]+))','URL',tweet)
        #Convert @username to AT_USER
        tweet = re.sub('@[^\s]+','AT_USER',tweet)
        #Remove additional white spaces
        tweet = re.sub('[\s]+', ' ', tweet)
        #Replace #word with word
        tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
        #trim
        return tweet
# Vanaf hier verranderen!!!! dit is vader en wat vanonder als comment erbij 
# staat hier overheen plakken voor textblob. Hier is een  
# Vergeet niet textblob en vader te instaleren via pip. ff googlen
       
    tweet_ids_lst = []
    tweet_text_lst = []
    
    tweet_sentiment_score = []
    counter = 0
    
    counterair += 1
    for key in Conversation.tweets.keys():
        if Conversation.tweets[key].user != user_id:
            tweet_ids_lst.append(key)
       # proc tweet cleant text
            proctweet = processTweet(Conversation.tweets[key].text)
            tweet_text_lst.append(proctweet)
       # snt is de 3 scores die vader output
            snt = analyser.polarity_scores(proctweet)
        # Dit haalt de sentiment comound score tussen -1 en 1 eruit
            tweet_sentiment_score.append(snt['compound'])
            print('sentiment: ', counter)
            counter += 1

tweet_sentiment_score


# Dus dit erover heen plakken,
"""
tweet_ids_lst = []
tweet_text_lst = []
tweet_sentiment_score = []
 
for key in Conversation.tweets.keys():
    tweet_ids_lst.append(key)
    
    proctweet = processTweet(Conversation.tweets[key].text)
    tweet_text_lst.append(proctweet)
    
    blob = TextBlob(proctweet)
    tweet_sentiment_score.append(blob.sentiment.polarity)
"""
            
            
            
            
            
            
            
            