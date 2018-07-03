# -*- coding: utf-8 -*-
"""
Created on Mon May 21 17:00:36 2018

@author: 20166843
"""

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
 
database = sqlite3.connect('data/mydb.sqlite3') #connect to database
 
#list of the user_id's per airline 
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
 
def incoming_volume_df_dates(user_name, airlines_id, date_start= "2016-03-01 00:00:00", date_end="2017-05-01 00:00:00"):
    """
    Gets the created_at of all incoming tweets
    :param user_name: String of the username of twitter user
    :param date_start: Datetime string in YYYY-MM-DD HH:MM:SS format
    :param date_end: Datetime string in YYYY-MM-DD HH:MM:SS format
    :return: Returns dataframe which contains created_at only
    """
 
    query = """
        SELECT created_at
        FROM tweets
        WHERE (text LIKE '%{}%' OR in_reply_to_user_id == {})
        AND datetime(created_at) >= datetime('{}')
        AND datetime(created_at) < datetime('{}');
            """.format(user_name, airlines_id, date_start, date_end)
 
    return pd.read_sql_query(query, database)
 
def outgoing_volume_df_dates(airlines_id, date_start= "2016-03-01 00:00:00", date_end="2017-05-01 00:00:00"):
    """
    Gets the created_at for the amount of tweets sent by the user in the given timespan
    :param user_id: String of ID of twitter user
    :param date_start: Datetime string in YYYY-MM-DD HH:MM:SS format
    :param date_end: Datetime string in YYYY-MM-DD HH:MM:SS format
    :return: Returns dataframe which contains created_at only
    """
    query = """SELECT created_at FROM tweets WHERE user_id == {} AND 
               (in_reply_to_user_id NOT NULL OR in_reply_to_tweet_id NOT NULL) AND
               datetime(created_at) >= datetime('{}') AND 
               datetime(created_at) < datetime('{}');""".format(airlines_id, date_start, date_end)
    
    return pd.read_sql_query(query, database)

#Run queries for incoming and outgoing volume for American Airlines             
data_incoming = incoming_volume_df_dates(user_name="AmericanAir", airlines_id= airlines["American_Air"])
data_outgoing = outgoing_volume_df_dates(airlines_id= airlines["American_Air"])

#create datetime objects
data_incoming['created_at'] = pd.to_datetime(data_incoming['created_at'])
data_outgoing['created_at'] = pd.to_datetime(data_outgoing['created_at']) 

#Count the tweets (incoming and outgoing) per day and store them in a dictionary {year, month:[days 1-31]}
counts_incoming = {}
counts_outgoing = {}
for year in [2016, 2017]:
    for month in range(12):
        print(month)
        month += 1
        month_list_incoming = []
        month_list_outgoing = []
        for day in range(31):
            day += 1
            month_list_incoming.append(data_incoming[(data_incoming['created_at'].dt.year == year) & (data_incoming['created_at'].dt.month == month) & (data_incoming['created_at'].dt.day == day)].count()[0])
            month_list_outgoing.append(data_outgoing[(data_outgoing['created_at'].dt.year == year) & (data_outgoing['created_at'].dt.month == month) & (data_outgoing['created_at'].dt.day == day)].count()[0])
        counts_incoming[str(year) + str(" ") + str(month)] = month_list_incoming
        counts_outgoing[str(year) + str(" ") + str(month)] = month_list_outgoing

# Pops months which we do not use in our database for incoming volume
counts_incoming.pop("2016 1")
counts_incoming.pop("2016 2")
counts_incoming.pop("2016 3")
counts_incoming.pop("2016 4")
counts_incoming.pop("2017 5")
counts_incoming.pop("2017 6")
counts_incoming.pop("2017 7")
counts_incoming.pop("2017 8")
counts_incoming.pop("2017 9")
counts_incoming.pop("2017 10")
counts_incoming.pop("2017 11")
counts_incoming.pop("2017 12")

#Convert to a nice dataframe 
df_incoming = pd.DataFrame(data=counts_incoming)
cols_incoming = list(df_incoming.columns.values)
cols_incoming = cols_incoming[3:8]+cols_incoming[0:3]+cols_incoming[8:]
df_incoming = df_incoming[cols_incoming]
df_incoming.index = range(1,32)
df_incoming.columns = ["May '16", "June '16", "July '16", "August '16", "September '16", "October '16", "November '16", "December '16", "January '17", "February '17", "March '17", "April '17"]

#make heatmap
sns.heatmap(df_incoming, linewidths=.5, cmap="Blues");
plt.xlabel("Months",size=13)
plt.ylabel("Days of the month", size=13)
plt.title('Incoming tweet volume by day for American Airlines', size=20);
plt.show()

# Pops months which we do not use in our database for outgoing volume
counts_outgoing.pop("2016 1")
counts_outgoing.pop("2016 2")
counts_outgoing.pop("2016 3")
counts_outgoing.pop("2016 4")
counts_outgoing.pop("2017 5")
counts_outgoing.pop("2017 6")
counts_outgoing.pop("2017 7")
counts_outgoing.pop("2017 8")
counts_outgoing.pop("2017 9")
counts_outgoing.pop("2017 10")
counts_outgoing.pop("2017 11")
counts_outgoing.pop("2017 12")

#Convert to a nice dataframe
df_outgoing = pd.DataFrame(data=counts_outgoing)
cols_outgoing = list(df_outgoing.columns.values)
cols_outgoing = cols_outgoing[3:8]+cols_outgoing[0:3]+cols_outgoing[8:]
df_outgoing = df_outgoing[cols_outgoing]
df_outgoing.index = range(1,32)
df_outgoing.columns = ["May '16", "June '16", "July '16", "August '16", "September '16", "October '16", "November '16", "December '16", "January '17", "February '17", "March '17", "April '17"]

#make heatmap
sns.heatmap(df_outgoing, linewidths=.5, cmap="GnBu");
plt.xlabel("Months",size=13)
plt.ylabel("Days of the month", size=13)
plt.title('Outgoing tweet volume by day for American Airlines', size=20);
plt.show()