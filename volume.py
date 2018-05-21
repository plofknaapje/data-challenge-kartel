# -*- coding: utf-8 -*-
"""
Created on Mon May 21 17:00:36 2018

@author: 20166843
"""

import sqlite3
import pandas as pd
import datetime
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
 
database = sqlite3.connect('data/mydb.sqlite3')
 
 
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
    Gets the amount of tweets which mention this user in the given timespan
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
 
data = incoming_volume_df_dates(user_name="AmericanAir", airlines_id= airlines["American_Air"])
 
data['created_at'] = pd.to_datetime(data['created_at'])
 
counts = {}
for year in [2016, 2017]:
    for month in range(12):
        print(month)
        month += 1
        month_list = []
        for day in range(31):
            day += 1
            month_list.append(data[(data['created_at'].dt.year == year) & (data['created_at'].dt.month == month) & (data['created_at'].dt.day == day)].count()[0])
       
        counts[str(year) + str(" ") + str(month)] = month_list 
counts.pop("2017 5")
print(counts)
df = pd.DataFrame(data=counts)
cols = list(df.columns.values)
cols = cols[3:8]+cols[0:3]+cols[8:]
df = df[cols]
df.index = range(1,32)
df = df.iloc[::-1]
df.columns = ["May '16", "June '16", "July '16", "August '16", "September '16", "October '16", "November '16", "December '16", "January '17", "February '17", "March '17", "April '17"]
sns.heatmap(df, linewidths=.5, cmap="Blues");
plt.xlabel("Months",size=13)
plt.ylabel("Days of the month", size=13)
plt.title('Incoming tweet volume by day for American Airlines', size=20);