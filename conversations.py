# -*- coding: utf-8 -*-
"""
Created on Tue May 22 15:47:09 2018

@author: 20166843
"""
from datetime import datetime, timedelta
import seaborn as sns; sns.set()
import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob
import re
import sqlite3
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

## Text
SMALL_SIZE = 14*2
MEDIUM_SIZE = 16*2
BIGGER_SIZE = 20*2

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

database = sqlite3.connect('data/mydb.sqlite3')

airlines_id = ["56377143", "106062176", "18332190", "22536055", "124476322", "26223583", "2182373406", "38676903",
               "1542862735", "253340062", "218730857", "45621423", "20626359"]
airlines_names = ["KLM", "AirFrance", "British_Airways", "AmericanAir", "Lufthansa", "AirBerlin", "AirBerlin assist",
                  "easyJet", "RyanAir", "SingaporeAir", "Qantas", "EtihadAirways", "VirginAtlantic"]
airlines_other_id = ["56377143", "106062176", "18332190", "124476322", "26223583", "2182373406", "38676903",
                     "1542862735", "253340062", "218730857", "45621423", "20626359"]
airlines_other_names = ["KLM", "AirFrance", "British_Airways", "Lufthansa", "AirBerlin", "AirBerlin assist", "easyJet",
                        "RyanAir", "SingaporeAir", "Qantas", "EtihadAirways", "VirginAtlantic"]
airlines_dict = {'56377143': 'KLM', '106062176': 'AirFrance', '18332190': 'British_Airways', '22536055': 'AmericanAir', '124476322': 'Lufthansa', '26223583': 'AirBerlin', '2182373406': 'AirBerlin assist', '38676903': 'easyJet', '1542862735': 'RyanAir', '253340062': 'SingaporeAir', '218730857': 'Qantas', '45621423': 'EtihadAirways', '20626359': 'VirginAtlantic'}

analyser = SentimentIntensityAnalyzer()

class Airline:
    
    """
    Contains all the Conversation objects for one airline and the methodes to
    change them all at the same time.
    """
    
    tweets = {}
    
    def __init__(self, user_name, user_id):
        """
        Initializes a new Airline Object
        :param user_name: str Twitter username of airline
        :param user_id: str Twitter userid of airline
        """
        self.name = user_name
        self.id = user_id
        self.reply_ids = []
        self.conversations = []
        self.tweets = []
        # Fills reply_ids list with the ids of tweets which have been replied to
        self.reply_ids = Airline.replyIdList()
        # Fills class tweets dict with Tweet object which are related to the airline
        self.addTweets()
        # Checks all Tweet objects and builds them into conversations
        self.makeConversations()
        # Executes sentiment analysis on all Conversation objects
        self.airlineSentimentDeltas()
        

    def addTweets(self, start_date = '2016-02-01 00:00:00', 
                  end_date = '2017-06-01 00:00:00'):
        """
        Adds all tweets as Tweet objects to the tweet list which:
            a. Were sent betweet start_date and end_date and
            b. Were either sent by the airline, a reply to the airline or 
                contains @user_name
        :param start_date: Datetime string to indicate starting moment
        :param end_date: Datetime string to indicate ending moment
        """
        query = """SELECT * FROM tweets WHERE (user_id == {} OR
            in_reply_to_user_id == {} OR text LIKE '%@{}%') AND
            datetime(created_at) >= datetime('{}') AND
            datetime(created_at) < datetime('{}');""".format(self.id, 
            self.id, self.name, start_date, end_date)
        cursor = database.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        database.commit()
        for row in result:
            tweet_id = row[0]
            created = row[1]
            user = row[2]
            text = row[3]
            reply_tweet = row[4]
            reply_user = row[5]
            lang = row[6]
            # Adds the tweet as Tweet object to the class dict tweets with id as key
            Airline.addTweetDict(tweet_id, user, text, created, lang,
                              reply_user, reply_tweet)
            # Adds the tweet id to the tweet list
            self.tweets.append(tweet_id)
            
        
    def getTweet(tweetid):
        """
        Checks if tweet with tweet_id exists in the database and adds it if possible
        :param tweetid: str tweet id
        :return: bool if tweet was added to class tweets dict
        """
        q = """SELECT * FROM tweets WHERE tweet_id == {}""".format(tweetid)
        cursor = database.cursor()
       
        try:
            cursor.execute(q)
            tweet = cursor.fetchall()[0]
            database.commit()
            """id, date, user, text, replt tweet, reply user, lang"""
            Airline.addTweetDict(tweet[0], tweet[2], tweet[3],
                                tweet[1], tweet[6], tweet[4], tweet[5])
            return True
        except:
            database.commit()
            return False

    
    def sentimentChanges(self):
        """
        Calls classify function and calculates sentiment change for each Conversation
        """
        Airline.classify()
        for conv in self.conversations:
            conv.sentimentChange(self.id)
    
    
    def makeConversations(self):
        """
        Checks all tweets for conversations
        Complexity: O(nlog(n))
        :return: Dictionary with conversation length frequencies
        """
        # For every tweet which was found by Conv.addTweets()
        for tweet_id in self.tweets: # o(n)
            # Only for tweets which were not replyed to, do:
            if not tweet_id in self.reply_ids: # O(1)
                conversation = Conversation(self.name, self.id) # O(1)
                conversation.addTweetConversation(tweet_id) # O(log(n))
                # Only save converations which are longer than 1 and contain interaction
                if conversation.length > 1 and conversation.containsUser():
                    self.conversations.append(conversation) # O(1)
        times = [len(conv) for conv in self.conversations] # O(n)
        self.conversationLengths = listToDict(times) # O(1)
    
    
    def airlineSentimentDeltas(self):
        """
        Runs sentimentDeltas on all conversations and combines the results into
        one dictionary.
        :return: dict with all interactions between airline and user with start
        and end sentiment and the delta
        """
        dict = {'user':[], 'start':[], 'end':[], 'delta':[]}
        for conv in self.conversations:
            sentChange = conv.sentimentDeltas(self.id)
            valdict = sentChange[0]
            isdict = sentChange[1]
            if isdict:
                for i in ['user', 'start', 'end', 'delta']:
                    dict[i] = dict[i] + valdict[i]
        return pd.DataFrame(dict)
    
    
    def replyRate(self):
        """
        
        
        """
        airline_reply_query =  """SELECT in_reply_to_tweet_id FROM tweets
        WHERE in_reply_to_tweet_id NOT NULL AND user_id == {};""".format(self.id)
        cursor = database.cursor()
        cursor.execute(airline_reply_query)
        result = cursor.fetchall()
        airline_reply = set([i[0] for i in result if i != 'None'])
        tweets = 0
        replies = 0
        for tweet in self.tweets:
            tweet = Airline.tweets[tweet]
            text = tweet.text
            if '@' + self.name in text:
                tweets = tweets + 1
                if tweet.tweet_id in airline_reply:
                    replies = replies + 1
        return [replies, tweets, replies/tweets]
        
    
    def classify():
        """
        Classifies all tweets in the Conversation.tweets dictionary
        """
        for id_ in Airline.tweets.keys():
            tweet = Airline.tweets[id_]
            if tweet.sentiment == None:
                tweet.sentimentScore()

    
    def addTweetDict(tweet_id, user, text, time, lang, 
                     reply_user = '', reply_tweet = ''):
        """
        Creates new Tweet object and adds it to the class tweet dict
        """
        Airline.tweets[tweet_id] = Tweet(tweet_id, user, text, time, 
                                      lang, reply_user, reply_tweet)


    def replyIdList():
        """
        Creates list with all the unique tweet_id's to which has been replied
        :return: set with str tweet ids
        """
        query = """SELECT in_reply_to_tweet_id FROM tweets
        WHERE in_reply_to_tweet_id NOT NULL;"""
        cursor = database.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        database.commit()
        return set([i[0] for i in result if i != 'None'])


class Conversation:
    
    """
    Class which contains a class dictionary with all relevant tweets as Tweet
    objects.
    Also contains a list with all tweets to which was replied.
    """
   
    def __init__(self, airline, id_):
        """
        Initializes basic variables of the object.
        :param tweets: optional dictionary to skip the building of the dict.
        """
        self.length = 0
        self.airline = airline
        self.id = id_
        self.tweets_lst = []
        
    
    def containsUser(self):
        """
        Checks if Conversation contains a tweet from airline
        :return: bool. contains tweet from airline
        """
        self.startingDate()
        contains = False
        for tweet in self.tweets_lst:
            tweet = Airline.tweets[tweet]
            if tweet.user == self.id:
                contains = True
        return contains
   
    
    def startingDate(self):
        """
        Computes starting Datetime of Conversation by finding the oldest tweet 
        saves the result in object variable
        """
        self.time = datetime.strptime('2017-06-01 00:00:00', '%Y-%m-%d %H:%M:%S')
        for tweet in self.tweets_lst:
            tweet = Airline.tweets[tweet]
            if tweet.time < self.time:
                self.time = tweet.time
    
    
    
                
    
    def addTweetConversation(self, tweet_id, end = False):
        """
        Adds a tweet to the tweet_lst and if tweet is a reply, recursively
        adds the replied to tweet. Sets length of conversation
        Complexity: Recursive -> log(n)
        :param tweet_id: str tweet_id of tweet to be added
        :param end: bool stops the recursion if True
        """
        
        tweet = Airline.tweets[tweet_id] # O(1)
        if end: # O(1)
            self.tweets_lst.append(tweet_id) # O(1)
        else: # O(1)
            self.tweets_lst = [tweet_id] + self.tweets_lst # O(1)
       
        tweet_id = tweet.reply_tweet # O(1)
        if tweet.reply_tweet in Airline.tweets.keys(): # O(1)
            self.addTweetConversation(tweet_id) # O(?)
        elif tweet_id != None:  # O(1)
            if Airline.getTweet(tweet_id) == True: # O(1)
                self.addTweetConversation(tweet_id) # O(1)
        self.length = len(self)
    
    
    def sentimentDeltas(self, airline_id):
        """
        Returns sentiment interactions in relation to airline_id
        Looks in conversation for the sequence user tweet, airline tweet, user tweet
        and reports the start sentiment, end sentiment, userid and delta of the sentiments.
        Complexity: O(mn) n = tweets in conversation, m = length of tweet
        :param airline_id: str of id to which the conversations are made.
        :return: list with the dict and True or 'No' and False
        """
        users = []
        tweets = []
        
        user_list = []
        start_list = []
        end_list = []
        delta_list = []
        
        for tweet in self.tweets_lst: # O(n)
            tweets.append(Airline.tweets[tweet]) # O(1)
            tweet = Airline.tweets[tweet] # O(1)
            user = tweet.user # O(1)
            if not user in users and not user == airline_id: # O(1)
                users.append(user) # O(1)
            if tweet.sentiment == None: # O(1)
                tweet.sentimentScore() # O(m)
                
        for user in users:
            start = None
            end = None
            intercept = False
            for tweet in tweets:
                tweet_user = tweet.user
                sentiment = tweet.sentiment
                if tweet_user == user:
                    if start == None or not intercept:
                        start = sentiment
                    elif intercept:
                        end = sentiment
                        delta = end - start
                        user_list.append(user)
                        start_list.append(start)
                        end_list.append(end)
                        delta_list.append(delta)
                        start = sentiment
                        intercept = False
                if tweet_user == airline_id and start != None:
                        intercept = True
        dict = {'user':user_list, 'start':start_list, 'end':end_list, 'delta':delta_list}
        if len(user_list) > 0:
            return [dict, True]
        else:
            return ['No', False]


    def sentimentChange(self, user_id):
        """
        Computes the sentiment change in conversation caused by interceptions 
        by user_id. Stores sentiment in object sentiment variable
        Complexity: O(mn)
        :param user_id: str user_id of user trying to influence sentiment
        """
        deltas = self.sentimentDeltas(user_id) # O(mn)
        if deltas[1]:
            self.sentiment = np.mean(deltas[0]['delta'])
        else:
            self.sentiment = None
        """
        if not self.sentiment == None: 
            for tweet in self.tweets_lst:
                tweet = Airline.tweets[tweet]
                # Finds first tweet after start or interception not by user
                if tweet.user != user_id and not interception:
                    before = tweet.sentiment
                # Checks for interception
                elif tweet.user == user_id:
                    interception = True
                # If intercept happened and there is a new tweet from not user,
                # Calculate the difference in sentiment
                elif tweet.user != user_id and interception:
                    if before != None:
                        changes.append(tweet.sentiment-before)
                    before = tweet.sentiment
                    interception = False
            if len(changes) > 0:
                self.sentiment = np.mean(changes)
        """
    

    def __len__(self):
        """
        Complexity: O(n)
        :return: int length of tweets_lst
        """
        if True:
            return len(self.tweets_lst)
        tweet = Airline.tweets[self.tweets_lst[0]]
        if tweet.reply_tweet != '':
            return len(self.tweets_lst) + 1
        elif tweet.user in airlines_id and tweet.reply_user != None:
            return len(self.tweets_lst) + 1
        else:
            return len(self.tweets_lst)


    def __return__(self):
        """
        :return: list Tweet object of tweet_ids in tweets_lst
        """
        return [Airline.tweets[tweet] for tweet in self.tweets_lst]
       
 
class Tweet:
   
    def __init__(self, tweet_id, user, text, time, lang, reply_user = '', reply_tweet = ''):
        """
        Creates new Tweet object and its variables
        Complexity: O(1)
        :param tweet_id: str of the tweet id
        :param user: str of user id
        :param text: str of tweet text
        :param reply_user: str of user id to which tweet replies or None
        :param reply_tweet: str of tweet id to which tweet replies or None
        :param time: str for datetime object in '%Y-%m-%d %H:%M:%S' format
        """
        self.tweet_id = tweet_id
        self.user = user
        self.text = text
        self.lang = lang
        self.reply_user = reply_user
        self.reply_tweet = reply_tweet
        self.time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S+00:00')
        self.sentiment = None
        
    
    def processTweet(self):
        """
        Cleans the text of the tweet
        Complexity: O(n)
        :return: str of cleaned tweet text
        """
        # process the tweets
        tweet = self.text
        #Convert to lower case
        tweet = tweet.lower()
        #Convert www.* or https?://* to URL
        tweet = re.sub('((www.[^\s]+)|(https?://[^\s]+))','URL',tweet)
        #Convert @username to AT_USER
        tweet = re.sub('@[^\s]+','AT_USER',tweet)
        #Remove additional white spaces
        tweet = re.sub('[\s]+', ' ', tweet)
        #Replace #word with word
        tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
        #trim
        return tweet
    
    
    def sentimentScore(self):
        """
        Scores the sentiment of a tweet with textblob
        Complexity: O(n)
        :return: float of sentiment of tweet between -1 and 1
        """
        text = self.processTweet() # O(n)
        blob = analyser.polarity_scores(text) # O(n)
        self.sentiment = blob['compound']
   
    def __str__(self):
        return 'ID:{} user:{} text:{} lang:{} reply_user:{} reply_tweet:{} created:{}'.format(self.tweet_id,
                   self.user, self.text, self.lang, self.reply_user, self.reply_tweet, self.time)
 
    
def listToDict(lst):
    """
    Turns a list into a dictionary with counts of duplicate text
    :param lst: List of ints or strings
    :return: Dictionary with counts of each unique item
    """
    dicti = {}
    for i in lst:
        if str(i) in dicti.keys():
            dicti[str(i)] = dicti[str(i)] + 1
        else:
            dicti[str(i)] = 1
    return dicti


def unrespondedTweets(airline):
    name = airline.name
    id = airline.id
    airline_reply_query =  """SELECT in_reply_to_tweet_id FROM tweets
    WHERE in_reply_to_tweet_id NOT NULL AND user_id == {};""".format(id)
    cursor = database.cursor()
    cursor.execute(airline_reply_query)
    result = cursor.fetchall()
    airline_reply = set([i[0] for i in result if i != 'None'])
    
    response = {'hour':[], 'reply':[], 'date':[]}
    
    for tweet in airline.tweets:
        tweet = Airline.tweets[tweet]
        if tweet.user != id and not tweet.tweet_id in airline_reply:
            dt = tweet.time
            if name == 'AmericanAir':
                dt = dt - timedelta(hours=6)
            response['hour'].append(dt.hour)
            response['date'].append(dt.strftime('%Y-%m-%d'))
            response['reply'].append(1)
    
    df = pd.DataFrame(response)
    amount_results = df.groupby(['date', 'hour']).size().reset_index().rename(columns={0:'count'})
    amount_results['date'] = pd.to_datetime(amount_results['date'],format='%Y-%m-%d')
    amount_results['day'] = amount_results['date'].dt.weekday
    amount_results.drop(['date'], axis=1)
    amount_results = amount_results.groupby(['day', 'hour']).median().reset_index()
    amount_results = amount_results.pivot('hour', 'day', 'count')
    
    fig, ax = plt.subplots(figsize=(22,16))
    sns.heatmap(amount_results, cmap='Blues', ax=ax, annot=amount_results,
                cbar_kws={'label': 'Amount of unanswered tweets'}, fmt='g')
    ax.invert_yaxis()
    plt.xlabel("Day of the week")
    plt.xticks([0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5], ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
    plt.ylabel("Hour of the day")
    plt.yticks([0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 11.5, 12.5,
            13.5, 14.5, 15.5, 16.5, 17.5, 18.5, 19.5, 20.5, 21.5, 22.5, 23.5],
           ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00",
            "07:00", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00",
            "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00",
            "21:00", "22:00", "23:00"], rotation=0)
    plt.plot()
    plt.show()


def lengthAmountGraph(airline_obj):
    datetimeLst = {'hour':[], 'length':[], 'date':[]}
    conversationList = airline_obj.conversations
    user_name = airline_obj.name
    for conv in conversationList:
        dt = conv.time
        if user_name == 'AmericanAir':
            dt = dt - timedelta(hours=6)
        datetimeLst['hour'].append(dt.hour)
        datetimeLst['date'].append(dt.strftime('%Y-%m-%d'))
        datetimeLst['length'].append(len(conv))

    df = pd.DataFrame(datetimeLst)
    amount_results = df.groupby(['date', 'hour']).size().reset_index().rename(columns={0:'count'})
    time_results = df.groupby(['date', 'hour']).median().reset_index().rename(columns={0:'length'})
    amount_results['date'] = pd.to_datetime(amount_results['date'],format='%Y-%m-%d')
    time_results['date'] = pd.to_datetime(time_results['date'], format='%Y-%m-%d')
    amount_results['day'] = amount_results['date'].dt.weekday
    time_results['day'] = amount_results['date'].dt.weekday
    amount_results.drop(['date'], axis=1)
    time_results.drop(['date'], axis=1)
    amount_results = amount_results.groupby(['day', 'hour']).median().reset_index()
    time_results = time_results.groupby(['day', 'hour']).median().reset_index()
    amount_results = amount_results.pivot('hour', 'day', 'count')
    time_results = time_results.pivot('hour', 'day', 'length')
    
    
    fig, ax = plt.subplots(figsize=(22,16))
    sns.heatmap(amount_results, cmap='Blues', vmin=0, vmax=48, ax=ax, 
                annot=amount_results, cbar_kws={'label': 'Median amount of conversations'})
    ax.invert_yaxis()
    plt.xlabel("Day of the week")
    plt.xticks([0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5], ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
    plt.ylabel("Hour of the day")
    plt.yticks([0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 11.5, 12.5,
            13.5, 14.5, 15.5, 16.5, 17.5, 18.5, 19.5, 20.5, 21.5, 22.5, 23.5],
           ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00",
            "07:00", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00",
            "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00",
            "21:00", "22:00", "23:00"], rotation=0)
    plt.plot()
    plt.show()


def lengthSentiment(airline):
    datetimeLst = {'sentiment':[], 'length':[]}
    bin = [-2, -0.66, -0.33, -0.0001, 0.0001, 0.33, 0.66, 2]
    labels = ['Very negative', 'Negative', 'Slightly negative', 'Neutral', 'Slightly positive', 'Positive', 'Very positive']
    conversationList = airline.conversations
    for conv in conversationList:
        conv.sentimentChange(airline.name)
        datetimeLst['sentiment'].append(conv.sentiment)
        datetimeLst['length'].append(conv.length)
    df = pd.DataFrame(datetimeLst)
    binned = pd.cut(df['sentiment'], bin, labels=labels)
    df['sentiment'] = binned
    labels.reverse()
    df = df.groupby('length')['sentiment'].value_counts().unstack().fillna(0)
    df = df.loc[:,labels]
    df = df.loc[range(3,11), :]
    df["sum"] = df.sum(axis=1)
    df_new = df.loc[:,labels].div(df["sum"], axis=0)
    df_new.plot.bar(stacked=True, figsize=(20,15),xlim=list([2,10]), cmap='RdYlBu')        
    legend_labels = ['Very Negative < -0.66', 'Negative < -0.33', 
                       'Slightly Negative < 0', 'Neutral = 0', 
                       'Slightly Positive > 0', 'Positive > 0.33', 
                       'Very Positive > 0.66']
    legend_labels.reverse()
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), 
               labels=legend_labels)
    plt.xlabel("Conversation length")
    plt.plot()
    plt.show()

if __name__ == "__main__":
    # execute only if run as a script
    airlines = {}
    airlineindex = 3
    airlineid = airlines_id[airlineindex]
    for airline in [airlines_id[airlineindex]]:
        airlines[airline] = Airline(airlines_dict[airline], airline)
        Airline.classify()
        df = airlines[airline].airlineSentimentDeltas() 

    for airline in list(airlines.keys()):
        airline = airlines[airline]
        print(airline.name)
        print(airline.conversationLengths)
    
    lengthAmountGraph(airlines[airlines_id[airlineindex]])
    
    unrespondedTweets(airlines[airlines_id[airlineindex]])
    
    lengthSentiment(airlines[airlines_id[airlineindex]])
    
    if False:
        datetimeLst = {'hour':[], 'sentiment':[], 'date':[]}
        conversationList = airlines[airlines_id[airlineindex]].conversations
        user_name = airlines_dict[airlineid]
        for conv in conversationList:
            dt = conv.time
            if user_name == 'AmericanAir':
                dt = dt - timedelta(hours=6)
            datetimeLst['hour'].append(dt.hour)
            datetimeLst['date'].append(dt.strftime('%Y-%m-%d'))
            lst = []
            for tweet in conv.tweets_lst:
                tweet = Airline.tweets[tweet]
                if tweet.user != airlineid:
                    lst.append(tweet.sentiment)
            sentiment = np.mean(lst)
            datetimeLst['sentiment'].append(sentiment)
    
        df = pd.DataFrame(datetimeLst)
        amount_results = df.groupby(['date', 'hour']).mean().reset_index().rename(columns={0:'sentiment'})
        amount_results['date'] = pd.to_datetime(amount_results['date'],format='%Y-%m-%d')
        amount_results['day'] = amount_results['date'].dt.weekday
        amount_results.drop(['date'], axis=1)
        amount_results = amount_results.groupby(['day', 'hour']).mean().reset_index()
        amount_results = amount_results.pivot('hour', 'day', 'sentiment')
        
        
        #amount_results[3][10] = amount_results[3].median()
        fig, ax = plt.subplots(figsize=(22, 18))
        sns.heatmap(amount_results, cmap='Blues', vmin=0)
        
        ax.invert_yaxis()
        plt.xlabel("day of the week")
        plt.xticks([0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5], ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
        plt.ylabel("hour of the day")
        plt.yticks([0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 11.5, 12.5,
                13.5, 14.5, 15.5, 16.5, 17.5, 18.5, 19.5, 20.5, 21.5, 22.5, 23.5],
               ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00",
                "07:00", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00",
                "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00",
                "21:00", "22:00", "23:00"], rotation=0)
        plt.plot()
        plt.show()
    # times = [len(conv) for conv in conversationList]
    
    if False:
        
    print(airlines[airlines_id[airlineindex]].replyRate())
    