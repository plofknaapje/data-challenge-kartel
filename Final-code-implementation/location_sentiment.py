# -*- coding: utf-8 -*-
"""
Created on Wed May 30 10:02:24 2018

@author: 20175876
"""
import gmaps
import gmaps.datasets
import sqlite3
import pandas as pd
import re
 
database = sqlite3.connect(r'C:\Users\20175876\Documents\GitHub\data-challenge-kartel\data\mydb.sqlite3')

#use API key to use gmaps
gmaps.configure(api_key="AIzaSyDHApYLQ71qXPCyplXzH2bkOlUUNDNWEYo")  

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

def get_coordinates(user_name, airlines_id, date_start= "2016-03-01 00:00:00", date_end="2017-05-01 00:00:00"):
    '''
    Gets the longitude, latitude for the amount of tweets sent by the user in the given timespan
    :param user_name: String of the username of twitter user
    :param airlines_id: String of ID of twitter user
    :param date_start: Datetime string in YYYY-MM-DD HH:MM:SS format
    :param date_end: Datetime string in YYYY-MM-DD HH:MM:SS format
    :return: Returns dataframe which contains the longitude, latitude and text of the incoming volume of a selected user
    '''
    query = """
        SELECT text, latitude, longitude
        FROM tweets
        WHERE (text LIKE '%{}%' OR in_reply_to_user_id == {})
        AND datetime(created_at) >= datetime('{}')
        AND datetime(created_at) < datetime('{}');
            """.format(user_name, airlines_id, date_start, date_end)
 
    return pd.read_sql_query(query, database)

#Longitude, latitude for incoming volume for American Air
df_aa = get_coordinates(user_name="American_Air", airlines_id= airlines["American_Air"])
df_aa = df_aa.dropna() #Only take non NaN values
df_aa #Only 525 tweets with location for American Airlines
df_aa_loc = df_aa[['latitude', 'longitude']]

#open sentiment file
df_sentiment = pd.read_csv(r'C:\Users\20175876\Documents\DC1 (1)\sentiment_AA.csv', sep=',')
df_sentiment = df_sentiment[['text', 'sentiment']]
df_sentiment.columns = ['new_text', 'sentiment']
df_sentiment.head() #815815 rows

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

#cleaned the text, new column called new_text
new_text = []
for tweet in df_aa.text:
    new_text.append(processTweet(tweet))

df_aa['new_text'] = new_text

#merge two dataframes
df_loc_sent = df_aa.merge(df_sentiment, how='outer', on='new_text')

df_loc_sent = df_loc_sent[['latitude', 'longitude', 'new_text', 'sentiment']] #remove old text
df_loc_sent.latitude.isnull().sum().sum() #813654
df_loc_sent.longitude.isnull().sum().sum() #813654
df_loc_sent.sentiment.isnull().sum().sum() #50

df_loc_sent = df_loc_sent.dropna(subset=['longitude', 'latitude', 'sentiment'])
df_loc_sent['sentiment'] = df_loc_sent['sentiment'] + 1 #gmap can only handle positve values
df_loc_sent.head() #4403 tweets

fig2 = gmaps.figure()
locations = df_loc_sent[['latitude', 'longitude']]
weights = df_loc_sent['sentiment']
fig2.add_layer(gmaps.heatmap_layer(locations, weights=weights, max_intensity=70, point_radius=5, opacity=0.5, gradient=[ 'white', 'red', 'green']))
fig2
