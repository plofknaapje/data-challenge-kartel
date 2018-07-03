# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 18:08:45 2018

@author: 20175876
"""

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import sqlite3
import re
import numpy as np
 
analyser = SentimentIntensityAnalyzer()
 
database = sqlite3.connect('data/myd.sqlite3')
 
 
 
airlines = {
    "KLM" : "56377143",
    "Air_France" : "106062176",
    "British_Airways" : "18332190",
    "American_Air" : "22536055",
    "Lufthansa" : "124476322",
    "Air_Berlin" : "26223583",
    "Air_Berlin_Assist": "2182373406",
    "easyJet": "38676903",
    "Ryanair": "1542862735",
    "Singapore_Air": "253340062",
    "Qantas": "218730857",
    "Etihad_Airways": "45621423",
    "Virgin_Atlantic": "20626359"}
 
def processTweet(tweet):
    """
    Cleans the text of the tweet
    :return: str of cleaned tweet text
    """
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
 
def get_coordinates(user_name, airlines_id):
    '''
    Gets the longitude, latitude for the amount of tweets sent by the user in the given timespan
    :param user_name: String of the username of twitter user
    :param airlines_id: String of ID of twitter user
    :return: Returns dataframe which contains the longitude and latitude of the incoming volume of a selected user
    '''
 
 
 
    query = """
        SELECT latitude, longitude, text
        FROM tweets
        WHERE (text LIKE '%{}%' OR in_reply_to_user_id == {});
            """.format(user_name, airlines_id)
 
    data = pd.read_sql_query(query, database)
 
    new_text = []
    for tweet in data['text']:
        new_text.append(processTweet(tweet))
   
    data['new_text'] = new_text
   
    sentiment = []
    for tweet in data['new_text']:
        vader = analyser.polarity_scores(tweet)
        vader2 = vader['compound']
        sentiment.append(vader2)
 
    data['sentiment'] = sentiment
   
    data = data.dropna(subset=['longitude', 'latitude', 'sentiment'])
   
   
    return(data)
   
data = get_coordinates(user_name="American_Air", airlines_id= airlines["American_Air"])
 
df_airports = pd.read_csv(r'C:\Users\20175876\Documents\DC1 (1)\airports.csv', header=None, sep=',')
df_airports.columns = ['airport_id', 'name', 'city', 'country', 'iata', 'icao', 'latitude', 'longitude', 'altitude', 'timezone', 'dst', 'tz', 'type airport', 'source']
df_airports_loc = df_airports[['longitude','latitude']]
 
df_airports_loc.head() #7184 airports
 
df_airports_loc.isnull().sum() #No missing values
 
airport_sentiment = []
non_airport_sentiment = []
 
for index, tweet in data.iterrows():
    for index, airport in df_airports_loc.iterrows():
        long = airport['longitude'] - tweet['longitude']
        lat =  airport['latitude'] - tweet['latitude']
        if np.sqrt(long**2+lat**2) < 0.2:
            airport_sentiment.append(tweet['text'])
        else:
            non_airport_sentiment.append(tweet['text'])
        
len(airport_sentiment)
len(non_airport_sentiment)
airport_sentiment

airport_sentiment
data