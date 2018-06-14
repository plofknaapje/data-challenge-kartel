# -*- coding: utf-8 -*-
"""
Created on Wed May 30 10:02:24 2018

@author: 20175876
"""
import gmaps
import gmaps.datasets
import numpy as np
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
 
database = sqlite3.connect('data/myd.sqlite3')

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
    :return: Returns dataframe which contains the longitude and latitude of the incoming volume of a selected user
    '''
    query = """
        SELECT latitude, longitude
        FROM tweets
        WHERE (text LIKE '%{}%' OR in_reply_to_user_id == {})
        AND datetime(created_at) >= datetime('{}')
        AND datetime(created_at) < datetime('{}');
            """.format(user_name, airlines_id, date_start, date_end)
 
    return pd.read_sql_query(query, database)

#Longitude, latitude for incoming volume for American Air
locations_df = get_coordinates(user_name="American_Air", airlines_id= airlines["American_Air"])
locations_df = locations_df.dropna() #Only take non NaN values
locations_df
fig = gmaps.figure()
fig.add_layer(gmaps.heatmap_layer(locations_df))
fig

 


