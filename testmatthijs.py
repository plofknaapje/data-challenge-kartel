# -*- coding: utf-8 -*-
"""
Created on Tue May 22 15:47:09 2018

@author: 20171877
"""
import access
from datetime import datetime, timedelta
import seaborn as sns;

sns.set()
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns;

sns.set()

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

# Default for AA
user_id = airlines_id[3]
user_name = airlines_names[3]

df = pd.read_csv('sentiment_airlines.csv')
df = df[df != 0]
print(df.columns)
plt.figure(figsize=[8,4])
print(len(df['AmericanAir'].dropna()))
sns.kdeplot(df['AmericanAir'].dropna(), bw=.1)
sns.kdeplot(df['British_Airways'].dropna(), bw=.1)
sns.kdeplot(df['RyanAir'].dropna(), bw=.1)
plt.show()
