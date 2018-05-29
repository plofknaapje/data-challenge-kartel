# Libs #
import access
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


"""
tweet_id TEXT PRIMARY KEY, 
created_at TEXT,
user_id TEXT, 
text TEXT, 
in_reply_to_tweet_id TEXT, 
in_reply_to_user_id TEXT, 
lang TEXT
"""

# Constants #
american_air_id = "22536055"
american_air = "AmericanAir"
database = access.db
airlines_id = ["56377143", "106062176", "18332190", "22536055", "124476322", "26223583", "2182373406", "38676903",
               "1542862735", "253340062", "218730857", "45621423", "20626359"]
airlines_names = ["KLM", "AirFrance", "British_Airways", "AmericanAir", "Lufthansa", "AirBerlin", "AirBerlin assist",
                  "easyJet", "RyanAir", "SingaporeAir", "Qantas", "EtihadAirways", "VirginAtlantic"]
airlines_other_id = ["56377143", "106062176", "18332190", "124476322", "26223583", "2182373406", "38676903",
                     "1542862735", "253340062", "218730857", "45621423", "20626359"]
airlines_other_names = ["KLM", "AirFrance", "British_Airways", "Lufthansa", "AirBerlin", "AirBerlin assist", "easyJet",
                        "RyanAir", "SingaporeAir", "Qantas", "EtihadAirways", "VirginAtlantic"]



def get_outgoing_volume(user_id, date_start, date_end):
    """
    Gets the amount of tweets sent by the user in the given timespan
    :param user_id: String of ID of twitter user
    :param date_start: Datetime string in YYYY-MM-DD HH:MM:SS format
    :param date_end: Datetime string in YYYY-MM-DD HH:MM:SS format
    :return: Amount of tweets which comply to all the requirements
    """
    query = """SELECT COUNT(*) FROM tweets WHERE user_id == {} AND 
               (in_reply_to_user_id NOT NULL OR in_reply_to_tweet_id NOT NULL) AND
               datetime(created_at) >= datetime('{}') AND 
               datetime(created_at) < datetime('{}');""".format(user_id, date_start, date_end)

    cursor = database.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    database.commit()
    return result


def get_incoming_volume(user_name, date_start, date_end):
    """
    Gets the amount of tweets which mention this user in the given timespan
    :param user_name: String of the username of twitter user
    :param date_start: Datetime string in YYYY-MM-DD HH:MM:SS format
    :param date_end: Datetime string in YYYY-MM-DD HH:MM:SS format
    :return: Amount of tweets which comply to all the requirements
    """

    query = """SELECT COUNT(*) FROM tweets WHERE text LIKE '%@{}%' AND 
               datetime(created_at) >= datetime('{}') AND 
               datetime(created_at) < datetime('{}');""".format(user_name, date_start, date_end)

    cursor = database.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    database.commit()
    return result


def volumes(user_id, user_name, start_date, end_date, interval_length):
    """
    Gets the amount of tweets from user_id and to user_name between start_date and end_date at interval lengths
    
    :param user_id: The id used for meassuring outgoing volume
    :param user_name: The name used for measuring incoming volume
    :param start_date: The date from which the count starts in YYYY-MM-DD HH:MM:SS format
    :param end_date: The date when the counting stops in YYYY-MM-DD HH:MM:SS format
    :param interval_length: The length of the intervals in days which the data is collected in.
    :return: A dataframe with columns for the startdate, incoming_volume, outgoing_volume, user_id and user_name
    """

    volume_dict = {'date':[], 'incoming_vol':[],'outgoing_vol':[], 'user_id':[], 'user_name':[]}
    
    
    """
    Datetime explanation:
        datetime.strptime(datetimestr, format) turns the datetimestr string into
        a datetime object according to the format.
        
        timedelta is a type of datetime object which can be added to a datetime object to increase it
        by a specific amount like 1 day or 1 week etc.
        
        When you have a datetime object dt, you can turn it into a string like so:
        dt.strftime(format) where it will return the given format."""
    
    ## Start and end are turned into datetime objects
    start = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
    end_date = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')
    ## The length of the interval is turned into a time delta to be added to the datetime objects
    delta = timedelta(days = interval_length)
    end = start + delta
    while start < end_date:
        ## Start and end datetime objects are used to create start and end strings
        start_str = start.strftime('%Y-%m-%d %H:%M:%S')
        end_str = end.strftime('%Y-%m-%d %H:%M:%S')
        volume_dict['date'].append(start_str)
        volume_dict['outgoing_vol'].append(get_outgoing_volume(user_id, start_str, end_str)[0][0])
        volume_dict['incoming_vol'].append(get_incoming_volume(user_name, start_str, end_str)[0][0])
        volume_dict['user_id'].append(user_id)
        volume_dict['user_name'].append(user_name)
        ## Start and end datetime objects are increased with the delta to prepare for the next interval
        start = start + delta
        end = end + delta

    
    df = pd.DataFrame(data=volume_dict)
    return df


def conversation_length(tweet_id, client_id, length=0):
    """
    Returns the length of the conversation from the tweet_id to its root
    :param tweet_id: ID of starting tweet
    :param client_id: ID of the user from whose perspective the length is generated
    :param length: Parameter for internal recordkeeping. Default is 0
    :return: Integer of the length of the conversation
    """
    q = "SELECT * FROM tweets WHERE tweet_id == {}".format(tweet_id)
    cursor = database.cursor()
    cursor.execute(q)
    try:
        tweet = cursor.fetchall()[0]
        database.commit()
        tweet_id = tweet[0]
        user_id = tweet[2]
        in_reply_to_tweet_id = tweet[4]
        ## If the tweet is not a reply to another tweet, it is either the begin or
        ## it is a reply to a user so the recursion gets broken.
        if in_reply_to_tweet_id is None:
            ## If the current user is our client, then the tweet is probably a 
            ## bad reply, so we count this tweet for two. Otherwise, it is the
            ## start tweet.
            if user_id == client_id:
                return length + 2
            else:
                return length + 1
        else:
            return conversation_length(in_reply_to_tweet_id, client_id, length) + 1
    ## Indexerror means no tweet was returned so the tweet is lost in an API mallfunction
    except IndexError:
        return length + 1


def conversations(client_id, client_name, start_date, end_date, use_name):
    """
    Returns the length of all the conversations which the client takes part in in the given timeframe.
    :param client_id: String of client ID
    :param client_name: String of client username
    :param start_date: String of starting date in %Y-%m-%d %H:%M:%S format
    :param end_date: String of starting date in %Y-%m-%d %H:%M:%S format
    :param use_name: Bool of whether to include tweets which contain @client_name
    :return: Dictionary with counts of conversation lengths
    """
    lengths = {}
    ## See volumes for a datetime explanation
    
    ## Start and end are datetime objects from the input variables.
    start = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
    end_date = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')
    ## Here, their scope is widened to account for long conversations
    start_ext = start - timedelta(days = 7)
    end_ext = end_date + timedelta(days = 7)
    ## Datetime strings are generated for use in the queries
    start_str = start.strftime('%Y-%m-%d %H:%M:%S')
    end_str = end_date.strftime('%Y-%m-%d %H:%M:%S')
    start_ext_str = start_ext.strftime('%Y-%m-%d %H:%M:%S')
    end_ext_str = end_ext.strftime('%Y-%m-%d %H:%M:%S')

    # Selects whether to include tweets with @client_name
    if use_name:
        q1 = """SELECT * FROM tweets WHERE (in_reply_to_tweet_id is NOT NULL OR in_reply_to_user_id IS NOT NULL ) AND
                       (text LIKE '%@{}%' OR user_id == {} OR in_reply_to_user_id == {}) AND
                       datetime(created_at) >= datetime('{}') AND 
                       datetime(created_at) < datetime('{}');""".format(client_name, client_id, client_id,
                                                                        start_str, end_str)
    else:
        q1 = """SELECT * FROM tweets WHERE (in_reply_to_tweet_id is NOT NULL OR in_reply_to_user_id IS NOT NULL ) AND
                              (user_id == {} OR in_reply_to_user_id == {}) AND
                              datetime(created_at) >= datetime('{}') AND 
                              datetime(created_at) < datetime('{}');""".format(client_id, client_id, start_str, end_str)
    cursor = database.cursor()
    cursor.execute(q1)
    result = cursor.fetchall()
    database.commit()

    # Selects all in_reply_to_tweet_id values in the given time span, with a 7 day extention on each side
    # to not exclude any tweets
    q2 = """SELECT DISTINCT(in_reply_to_tweet_id) FROM tweets WHERE in_reply_to_tweet_id is NOT NULL AND
                       datetime(created_at) >= datetime('{}') AND 
                       datetime(created_at) < datetime('{}');""".format(start_ext_str, end_ext_str)
    cursor = database.cursor()
    cursor.execute(q2)

    # Query converted to Pandas DataFrame to extract all values
    df = pd.DataFrame(cursor.fetchall(), columns=['val'])
    in_reply_to_ids = df['val'].values
    database.commit()
    for tweet in result:
        tweet_id = tweet[0]
        # If the tweet_id can be found in an in_reply_to_ids, then it is not the last tweet of a conversation
        if tweet_id in in_reply_to_ids:
            continue
        length = conversation_length(tweet_id, client_id)
        if length != 1:
            try:
                lengths[length] = lengths[length] + 1
            except KeyError:
                lengths[length] = 1
    return lengths

i = 0
volume = {'airline':[], 'incoming':[], 'outgoing':[]}
while i < len(airlines_id):
    print(i)
    name = airlines_names[i]
    id_ = airlines_id[i]
    volume['airline'].append(name)
    volume['incoming'].append(get_incoming_volume(name, date_start = '2016-02-01 00:00:00', date_end = '2017-06-01 00:00:00')[0][0])
    volume['outgoing'].append(get_outgoing_volume(id_, date_start = '2016-02-01 00:00:00', date_end = '2017-06-01 00:00:00')[0][0])
    i = i + 1


df = pd.DataFrame(volume)

df.plot(x='airline', y='incoming', kind='bar')
df.plot(x='airline', y='outgoing', kind='bar')

# print(get_volume(american_air_id, '2016-05-30 00:00:00', '2016-12-11 00:00:00'))
# print(volumes(american_air_id, american_air, '2016-05-30 00:00:00', '2017-05-01 00:00:00', 7))

#print(volumes(american_air_id, american_air, '2016-05-30 00:00:00', '2016-08-01 00:00:00', 7))
#print(find_origin_tweet('757691415958843392', american_air_id, 0))

#print(conversations(american_air_id, american_air, '2016-05-30 00:00:00', '2017-05-01 00:00:00', False))
"""
@Robin why is this block of code in here?
if True:
    data = {'week':[], 'conversations':[]}
    week = 1
    date = datetime.strptime('2016-05-30 00:00:00', '%Y-%m-%d %H:%M:%S')
    date_end = datetime.strptime('2016-05-30 00:00:00', '%Y-%m-%d %H:%M:%S') + timedelta(days=7)
    date_str = datetime.strftime(date, '%Y-%m-%d %H:%M:%S')
    date_end_str = datetime.strftime(date_end, '%Y-%m-%d %H:%M:%S')
    while week < 52:
        convs = conversations(american_air_id, american_air, date_str, date_end_str, False)
        total = sum(convs)
        data['week'].append(week)
        data['conversations'].append(convs)
        week = week + 1
        date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S') + timedelta(days=7)
        date_end = datetime.strptime(date_end_str, '%Y-%m-%d %H:%M:%S') + timedelta(days=7)
        date_str = datetime.strftime(date, '%Y-%m-%d %H:%M:%S')
        date_end_str = datetime.strftime(date_end, '%Y-%m-%d %H:%M:%S')
        print(week)

    print(data)
"""




database.close()
