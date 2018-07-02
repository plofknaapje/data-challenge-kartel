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
    df['KLM'].value_counts()

df1 = df3.apply(pd.value_counts)    
df1
df['KLM']
df['test']
df1[['AmericanAir','British_Airways','RyanAir','KLM','easyJet']]
totals = [a, b, c, d, e, f, g for a, b, c, d, e, f, g in zip(df[])]

r = ['American Air','British Airways','RyanAir','KLM','EasyJet']
raw_data = {'vnega': [6682, 3895, 1457, 900, 2214], 'nega': [104444, 62514, 13985, 7157, 21491],'snega': [71770, 47277, 19153, 8708, 22899], 'neutral': [321945, 201640, 125372, 138946, 92859], 'spos':[134383, 88153, 31457, 38243, 28032], 'pos':[133073, 93029, 57818, 39360, 26021], 'vpos' :[30290, 32329, 15183, 9512, 5319]}
df3 = pd.DataFrame(raw_data)
df3
# From raw value to percentage
totals = [i+j+k+l+m+n+o for i,j,k,l,m,n,o in zip(df3['vnega'], df3['nega'], df3['snega'], df3['neutral'], df3['spos'],df3['pos'],df3['vpos'])]
vnega = [i / j * 100 for i,j in zip(df3['vnega'], totals)]
nega = [i / j * 100 for i,j in zip(df3['nega'], totals)]
snega = [i / j * 100 for i,j in zip(df3['snega'], totals)]
neutral = [i / j * 100 for i,j in zip(df3['neutral'], totals)]
spos = [i / j * 100 for i,j in zip(df3['spos'], totals)]
pos = [i / j * 100 for i,j in zip(df3['pos'], totals)]
vpos = [i / j * 100 for i,j in zip(df3['vpos'], totals)]

# plot
barWidth = 0.85
names = ('American Air','British Airways','RyanAir','KLM','EasyJet')


plt.bar(r, vnega, color='#601204', edgecolor='white', width=barWidth)


plt.bar(r, nega, bottom=vnega, color='#c02408', edgecolor='white', width=barWidth)


plt.bar(r, snega, bottom=[i+j for i,j in zip(vnega, nega)], color='#f3573b', edgecolor='white', width=barWidth)


plt.bar(r, neutral, bottom=[i+j+k for i,j,k in zip(vnega, nega, snega)], color='#EAD57E', edgecolor='white', width=barWidth)
                             
plt.bar(r, spos, bottom=[i+j+k+l for i,j,k,l in zip(vnega, nega, snega, neutral)], color='#66c166', edgecolor='white', width=barWidth)


plt.bar(r, pos, bottom=[i+j+k+l+m for i,j,k,l,m in zip(vnega, nega, snega, neutral, spos)], color='#009900', edgecolor='white', width=barWidth)
                             
plt.bar(r, vpos, bottom=[i+j+k+l+m+n for i,j,k,l,m,n in zip(vnega, nega, snega, neutral, spos, pos)], color='#004C00', edgecolor='white', width=barWidth)


                             
plt.xticks(r, names)
plt.xlabel("Airlines")
 
# Show graphic
plt.show()

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