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
df3 = pd.read_csv('labeled_sentiment.csv', low_memory=False)


    
for airline in df3:
    df3[airline].value_counts()
#    df['KLM'].value_counts()

df1 = df3.apply(pd.value_counts)    
print(df1)
#Gather the value counts with the above code.

"""
We counted all the words with the above code, and then we
put all the counts per sentiment into the code by hand.
This is kind of redundant but this was the most convenient way
to do it at the time

Below the code produces a stackedbar plot with the sentiment-
distribution for all the airlines.

"""

fig, ax = plt.subplots(figsize=(20,10))
data = {'VeryNegative': [2351,1404,12767,29265,2273,1336,6730,4201,513,1461,1202,1735], 'Negative': [21869, 12862,121278,209649,19361,9483,55515,38914,4399,12749,8320,14524],'SlightlyNegative': [4839, 3134,25139,40810,3542,1372,12405,13308,879,3290,2185,4014],'Neutral': [120325, 47756, 141223,217281,45099,18767,60397,91489,20479,33085,40074,31904], 'SligthlyPositive': [7323, 3816,28965,44903,5105,1900,11946,13145,2104,5199,4498,5498], 'Positive': [73742, 16368,163219,221106,25197,6638,46001,65683,18245,37137,35280,36789], 'VeryPositive': [13014, 4837,41054,52801,5585,943,8581,39267,6220,20115,11694,11679]}
df = pd.DataFrame(data)
r = ['KLM', 'AirFrance', 'BritishAirways', 'AmericanAir', 'Lufthansa', 'AirBerlin',  'EasyJet', 'RyanAir', 'SingaporeAir', 'QuantasAir', 'EtihadAirways', 'VirginAtlantic']
 
 
totals = [i+j+k+l+m+n+o for i,j,k,l,m,n,o in zip(df['VeryNegative'], df['Negative'], df['SlightlyNegative'], df['Neutral'], df['SligthlyPositive'], df['Positive'], df['VeryPositive'])]
VeryNegative = [i / j * 100 for i,j in zip(df['VeryNegative'], totals)]
Negative = [i / j * 100 for i,j in zip(df['Negative'], totals)]
SligthlyNegative = [i / j * 100 for i,j in zip(df['SlightlyNegative'], totals)]
Neutral = [i / j * 100 for i,j in zip(df['Neutral'], totals)]
SlightlyPositive = [i / j * 100 for i,j in zip(df['SligthlyPositive'], totals)]
Positive = [i / j * 100 for i,j in zip(df['Positive'], totals)]
VeryPositive = [i / j * 100 for i,j in zip(df['VeryPositive'], totals)]
 
barWidth = 0.85
names = ('KLM', 'AirFrance', 'BritishAirways', 'AmericanAir', 'Lufthansa', 'AirBerlin', 'EasyJet', 'RyanAir', 'SingaporeAir', 'QuantasAir', 'EtihadAirways', 'VirginAtlantic')
# Create green Bars
plt.bar(r, VeryNegative, color='#601204', edgecolor='white', width=barWidth)
 
plt.bar(r, Negative, bottom=VeryNegative, color='#c02408', edgecolor='white', width=barWidth)
 
plt.bar(r, SligthlyNegative, bottom=[i+j for i,j in zip(VeryNegative, Negative)], color='#f3573b', edgecolor='white', width=barWidth)
 
plt.bar(r, Neutral, bottom=[i+j+k for i,j,k in zip(VeryNegative, Negative, SligthlyNegative)], color='#EAD57E', edgecolor='white', width=barWidth)
                             
plt.bar(r, SlightlyPositive, bottom=[i+j+k+l for i,j,k,l in zip(VeryNegative, Negative, SligthlyNegative, Neutral)], color='#66c166', edgecolor='white', width=barWidth)
 
plt.bar(r, Positive, bottom=[i+j+k+l+m for i,j,k,l,m in zip(VeryNegative, Negative, SligthlyNegative, Neutral, SlightlyPositive)], color='#009900', edgecolor='white', width=barWidth)
                             
plt.bar(r, VeryPositive, bottom=[i+j+k+l+m+n for i,j,k,l,m,n in zip(VeryNegative, Negative, SligthlyNegative, Neutral, SlightlyPositive, Positive)], color='#004C00', edgecolor='white', width=barWidth)
                             
plt.xticks(r, names)
plt.xlabel("Airlines")
 
# Show graphic
plt.show()