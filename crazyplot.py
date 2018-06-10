# -- coding: utf-8 --
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
    total = 0
    for sentiment in airline:
        summ += sentiment
        sentiment = sentiment/summ
    print(airline, summ)
 
data = {'VeryNegative': [900,793,3895,6682,491,300,37,2214,1457,164,632,361,663], 'Negative': [7157, 4042,62514,104444,4829,2439,308,21491,13985,1759,5575,3489,6594],'SlightlyNegative': [8708, 4523,47277,71770,7070,2184,282,22899,19153,2362,6835,5693,7229],'Neutral': [138946, 57280, 201640,321945,58323,24048,2107,92859,125372,24087,38308,47157,42481], 'SligthlyPositive': [38243, 11210,88153,134383,15770,3625,432,28032,31457,7538,20131,15679,19409], 'Positive': [39360, 9373,93029,133073,15248,3508,337,26021,57818,13426,35532,21868,23468], 'VeryPositive': [9512, 2306,32329,30290,3893,505,37,5319,15183,3315,5628,8502,5705]}
df = pd.DataFrame(data)
r = ['KLM', 'AirFrance', 'BritishAirways', 'AmericanAir', 'Lufthansa', 'AirBerlin', 'AirberlinAssist', 'EasyJet', 'RyanAir', 'SingaporeAir', 'QuantasAir', 'EtihadAirways', 'VirginAtlantic']
 
 
totals = [i+j+k+l+m+n+o for i,j,k,l,m,n,o in zip(df['VeryNegative'], df['Negative'], df['SlightlyNegative'], df['Neutral'], df['SligthlyPositive'], df['Positive'], df['VeryPositive'])]
VeryNegative = [i / j * 100 for i,j in zip(df['VeryNegative'], totals)]
Negative = [i / j * 100 for i,j in zip(df['Negative'], totals)]
SligthlyNegative = [i / j * 100 for i,j in zip(df['SlightlyNegative'], totals)]
Neutral = [i / j * 100 for i,j in zip(df['Neutral'], totals)]
SlightlyPositive = [i / j * 100 for i,j in zip(df['SligthlyPositive'], totals)]
Positive = [i / j * 100 for i,j in zip(df['Positive'], totals)]
VeryPositive = [i / j * 100 for i,j in zip(df['VeryPositive'], totals)]
 
barWidth = 0.85
names = ('KLM', 'AirFrance', 'BritishAirways', 'AmericanAir', 'Lufthansa', 'AirBerlin', 'AirberlinAssist', 'EasyJet', 'RyanAir', 'SingaporeAir', 'QuantasAir', 'EtihadAirways', 'VirginAtlantic')
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