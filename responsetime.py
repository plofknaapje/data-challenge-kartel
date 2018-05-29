# libs #
import access
import sqlite3
import pandas as pd
import numpy as np
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

"""
tweet_id text primary key, 
created_at text,
user_id text, 
text text, 
in_reply_to_tweet_id text, 
in_reply_to_user_id text, 
lang text
"""

# constants #
american_air_id = "22536055"
american_air = "americanair"
database = access.db
airlines_id = ["56377143", "106062176", "18332190", "22536055", "124476322", "26223583", "2182373406", "38676903",
               "1542862735", "253340062", "218730857", "45621423", "20626359"]
airlines_names = ["klm", "airfrance", "british_airways", "americanair", "lufthansa", "airberlin", "airberlin assist",
                  "easyjet", "ryanair", "singaporeair", "qantas", "etihadairways", "virginatlantic"]
airlines_other_id = ["56377143", "106062176", "18332190", "124476322", "26223583", "2182373406", "38676903",
                     "1542862735", "253340062", "218730857", "45621423", "20626359"]
airlines_other_names = ["klm", "airfrance", "british_airways", "lufthansa", "airberlin", "airberlin assist", "easyjet",
                        "ryanair", "singaporeair", "qantas", "etihadairways", "virginatlantic"]



def response_time(airline, timevar):
    """
    prints the mean response time of a certain airline in a certain month
    :param airline: id of the airline
    :param month: integer of the month
    :return: mean response time of an airline in a certain month
    """

    query1 = """select * from tweets where user_id = '{}' and 
                in_reply_to_tweet_id is not null """.format(airline)

    query2 = """select * from tweets where in_reply_to_user_id = '{}' """.format(airline)

    tweet_airline = pd.read_sql_query(query1, database)
    tweet_customer = pd.read_sql_query(query2, database)

    conn = sqlite3.connect('response_time.db')

    tweet_airline.to_sql('airline', conn, if_exists='replace')
    tweet_customer.to_sql('customer', conn, if_exists='replace')

    query3 = """select airline.in_reply_to_tweet_id, airline.created_at as 
                airline_time, customer.tweet_id, customer.created_at as customer_time
                from airline, customer where airline.in_reply_to_tweet_id = customer.tweet_id and 
                datetime(airline.created_at) > datetime(customer.created_at) """

    tweet_link = pd.read_sql_query(query3, conn)
    tweet_link['response_time'] = 0
    tweet_link['airline_time'] = pd.to_datetime(tweet_link['airline_time'])
    tweet_link['customer_time'] = pd.to_datetime(tweet_link['customer_time'])
    # for the code below, comment out what you dont need
    # tweet_link = tweet_link[tweet_link['airline_time'].dt.month == timevar] # for calculating per month
    # tweet_link = tweet_link[tweet_link['airline_time'].dt.weekday == timevar] # for calculating per day of the week
    # tweet_link = tweet_link[tweet_link['airline_time'].dt.hour == timevar] # for calculating per hour
    tweet_link['response_time'] = tweet_link['airline_time'] - tweet_link['customer_time']
    tweet_link['response_time'] = tweet_link['response_time'] / np.timedelta64(1, 's')
    tweet_link['weekday'] = tweet_link['customer_time'].dt.weekday
    tweet_link['hour'] = tweet_link['customer_time'].dt.hour
    conversation_day_hour = tweet_link.groupby(['weekday', 'hour']).median().reset_index()
    #conversation_day_hour['response_time'] = tweet_link.groupby(['weekday', 'hour']).median()
    return conversation_day_hour
    #return tweet_link['response_time'].median()


#print(response_time('22536055', 1))
plt.figure(figsize=[8,4])
sns.heatmap(response_time('22536055', 1).pivot('hour', 'weekday', 'response_time'), cmap="Blues")
plt.xlabel("day of the week")
plt.xticks([0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5], ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
plt.ylabel("hour of the day")
plt.yticks([0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 11.5, 12.5,
            13.5, 14.5, 15.5, 16.5, 17.5, 18.5, 19.5, 20.5, 21.5, 22.5, 23.5],
           ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00",
            "07:00", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00",
            "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00",
            "21:00", "22:00", "23:00"], rotation=0)
plt.show()
# below is the for loop for response times per month of the day per airline
"""for x in range (0,12):
    print(response_time("20626359",x)"""
# all airline data are in the excel file in the folder

# below are response times per day of the week in the order: mo,tu,we,thu,fr,sat,sun
reptimeperday = [1573.0, 1175.0, 936.0, 1475.0, 1826.0, 1273.0, 1178.0]
"""for i in range(0,7):
    reptimeperday.append(response_time("22536055", i))
print(reptimeperday)
"""
reptimeperhour = [1704.0, 1882.0, 1552.0, 1350.0, 993.0, 873.0, 951.0, 725.0, 588.0, 345.0, 304.0, 487.5,
                  693.5, 813.0, 1031.0, 1304.0, 1489.0, 1613.5, 1597.0, 1701.0, 1847.0, 1749.0, 1673.0, 1719.0]
"""for i in range(0,24):
    reptimeperhour.append(response_time("22536055", i))
"""
#print(reptimeperhour)
