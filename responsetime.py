# Libs #
import access
import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def response_time(airline, month):
    """
    Prints the mean response time of a certain airline in a certain month
    :param airline: ID of the airline
    :param month: Integer of the month
    :return: Mean response time of an airline in a certain month
    """

    query1 = """SELECT * FROM tweets WHERE user_id = '{}' AND 
                in_reply_to_tweet_id IS NOT NULL """.format(airline)

    query2 = """SELECT * FROM tweets WHERE in_reply_to_user_id = '{}' """.format(airline)

    tweet_airline = pd.read_sql_query(query1, database)
    tweet_customer = pd.read_sql_query(query2, database)

    conn = sqlite3.connect('response_time.db')

    tweet_airline.to_sql('airline', conn, if_exists='replace')
    tweet_customer.to_sql('customer', conn, if_exists='replace')

    query3 = """SELECT airline.in_reply_to_tweet_id, airline.created_at as 
                airline_time, customer.tweet_id, customer.created_at as customer_time
                FROM airline, customer WHERE airline.in_reply_to_tweet_id = customer.tweet_id AND 
                airline.created_at > customer.created_at """

    tweet_link = pd.read_sql_query(query3, conn)
    tweet_link['response_time'] = 0
    tweet_link['airline_time'] = pd.to_datetime(tweet_link['airline_time'])
    tweet_link['customer_time'] = pd.to_datetime(tweet_link['customer_time'])
    # For the code below, comment out what you DONT need
    # tweet_link = tweet_link[tweet_link['airline_time'].dt.month == month] # For calculating per month
    # tweet_link = tweet_link[tweet_link['airline_time'].dt.weekday == month] # For calculating per day of the week
    tweet_link = tweet_link[tweet_link['airline_time'].dt.hour == month] # For calculating per hour
    tweet_link['response_time'] = tweet_link['airline_time'] - tweet_link['customer_time']
    tweet_link['response_time'] = tweet_link['response_time'] / np.timedelta64(1, 's')
    return tweet_link['response_time'].median()


# Below are response times per day of the week in the order: mo,tu,we,thu,fr,sat,sun
reptimeperday = [1573.0, 1175.0, 936.0, 1475.0, 1826.0, 1273.0, 1178.0]
"""for i in range(0,7):
    reptimeperday.append(response_time("22536055", i))
print(reptimeperday)
"""
reptimeperhour = [1704.0, 1882.0, 1552.0, 1350.0, 993.0, 873.0, 951.0, 725.0, 588.0, 345.0, 304.0, 487.5,
                  693.5, 813.0, 1031.0, 1304.0, 1489.0, 1613.5, 1597.0, 1701.0, 1847.0, 1749.0, 1673.0, 1719.0]
for i in range(0,24):
    reptimeperhour.append(response_time("22536055", i))
print(reptimeperhour)
