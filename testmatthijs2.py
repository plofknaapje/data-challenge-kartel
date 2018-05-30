# -*- coding: utf-8 -*-
"""
Created on Tue May 22 15:47:09 2018

@author: 20171877
"""
import access
from datetime import datetime, timedelta
import seaborn as sns

sns.set()
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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

disclist = []
df = pd.read_csv('labeled_sentiment.csv', low_memory=False)
for airline in df:
    disclist.append(df[airline].value_counts().sort_values())
del disclist[0]


for airline in disclist:
    summ = 0
    for sentiment in airline:
        summ += sentiment
        sentiment = sentiment/summ
    print(airline, summ)

plt.show()