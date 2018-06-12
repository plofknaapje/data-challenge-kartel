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
# change here to edit which airline you want to see

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
        #self.sentimentChanges()
        

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
        :return: Dictionary with conversation length frequencies
        """
        # For every tweet which was found by Conv.addTweets()
        for tweet_id in self.tweets:
            # Only for tweets which were not replyed to, do:
            if not tweet_id in self.reply_ids:
                conversation = Conversation(self.name, self.id)
                conversation.addTweetConversation(tweet_id)
                # Only save converations which are longer than 1 and contain interaction
                if conversation.length > 1 and conversation.containsUser():
                    self.conversations.append(conversation)
        times = [len(conv) for conv in self.conversations]
        self.conversationLengths = listToDict(times)
    
    
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
    
    
    def sentimentChange(self, user_id):
        """
        Computes the sentiment change in conversation caused by interceptions 
        by user_id. Stores sentiment in object sentiment variable
        :param user_id: str user_id of user trying to influence sentiment
        """
        before = None
        interception = False
        changes = []
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
        else:
            self.sentiment = None
                
    
    def addTweetConversation(self, tweet_id, end = False):
        """
        Adds a tweet to the tweet_lst and if tweet is a reply, recursively
        adds the replied to tweet. Sets length of conversation
        :param tweet_id: str tweet_id of tweet to be added
        :param end: bool stops the recursion if True
        """
        
        tweet = Airline.tweets[tweet_id]
        if end:
            self.tweets_lst.append(tweet_id)
        else:
            self.tweets_lst = [tweet_id] + self.tweets_lst
       
        tweet_id = tweet.reply_tweet
        if tweet.reply_tweet in Airline.tweets.keys():
            self.addTweetConversation(tweet_id)
        elif tweet_id != None:
            if Airline.getTweet(tweet_id) == True:
                self.addTweetConversation(tweet_id)
        self.length = len(self)
    
    
    def sentimentDeltas(self, airline_id):
        """
        Returns sentiment interactions in relation to airline_id
        Looks in conversation for the sequence user tweet, airline tweet, user tweet
        and reports the start sentiment, end sentiment, userid and delta of the sentiments.
        :param airline_id: str of id to which the conversations are made.
        :return: list with the dict and True or 'No' and False
        """
        users = []
        tweets = []
        
        user_list = []
        start_list = []
        end_list = []
        delta_list = []
        
        for tweet in self.tweets_lst:
            tweets.append(Airline.tweets[tweet])
            tweet = Airline.tweets[tweet]
            user = tweet.user
            if not user in users and not user == airline_id:
                users.append(user)
            if tweet.sentiment == None:
                tweet.sentimentScore()
                
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


    def __len__(self):
        """
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
        :return: float of sentiment of tweet between -1 and 1
        """
        text = self.processTweet()
        blob = TextBlob(text)
        self.sentiment = blob.sentiment.polarity
   
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


if __name__ == "__main__":
    # execute only if run as a script
    airlines = {}
    for airline in [airlines_id[5]]:
        airlines[airline] = Airline(airlines_dict[airline], airline)
        Airline.classify()
        df = airlines[airline].airlineSentimentDeltas() 

    for airline in list(airlines.keys()):
        airline = airlines[airline]
        print(airline.name)
        print(airline.conversationLengths)
    
    conv = airlines['26223583'].conversations[0]
    print(conv.sentimentDeltas(airlines_id[5]))
    if False:
        datetimeLst = {'hour':[], 'length':[], 'date':[]}
        for conv in conversationList:
            dt = conv.time
            if user_name == 'AmericanAir':
                dt = dt - timedelta(hours=6)
            datetimeLst['hour'].append(dt.hour)
            datetimeLst['date'].append(dt.strftime('%Y-%m-%d'))
            datetimeLst['length'].append(conv.length)
    
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
        
        
        fig, ax = plt.subplots(figsize=(10,5))
        sns.heatmap(amount_results, cmap='Blues', vmin=0, vmax=48, ax=ax, annot=time_results)
        # ax.invert_yaxis()
        plt.xlabel("day of the week")
        plt.xticks([0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5], ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
        plt.ylabel("hour of the day")
        plt.yticks([0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 11.5, 12.5,
                13.5, 14.5, 15.5, 16.5, 17.5, 18.5, 19.5, 20.5, 21.5, 22.5, 23.5],
               ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00",
                "07:00", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00",
                "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00",
                "21:00", "22:00", "23:00"], rotation=0)
        plt.title('Median amount of conversation with {}'.format(user_name))
        plt.plot()
        plt.show()
    
        for tweet in conversationList[1].tweets_lst:
            tweet = Conversation.tweets[tweet]
            print(tweet.user, tweet.sentiment)
        conversationList[2].sentimentChange()
        print(conversationList[2].sentiment)
    
        tweet = list(Conversation.tweets.keys())[0]
        print(Conversation.tweets[tweet].sentiment   ) 
        
    if False:
        datetimeLst = {'hour':[], 'sentiment':[], 'date':[]}
        for conv in conversationList:
            dt = conv.time
            if user_name == 'AmericanAir':
                dt = dt - timedelta(hours=6)
            datetimeLst['hour'].append(dt.hour)
            datetimeLst['date'].append(dt.strftime('%Y-%m-%d'))
            lst = []
            for tweet in conv.tweets_lst:
                tweet = Conversation.tweets[tweet]
                if tweet.user != user_id:
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
        fig, ax = plt.subplots(figsize=(10,5))
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
        plt.title('Mean sentiment of users in conversation with {}'.format(user_name))
        plt.plot()
        plt.show()
    # times = [len(conv) for conv in conversationList]
    
    if False:
        datetimeLst = {'sentiment':[], 'length':[]}
        bin = [-1, -0.75, -0.25, -0.0001, 0.0001, 0.25, 0.75, 1]
        labels = ['Very negative', 'Negative', 'Slightly negative', 'Neutral', 'Slightly positive', 'Positive', 'Very positive']
        conversationList = airlines['22536055']
        for conv in conversationList:
            tweet = conv.tweets_lst[0]
            tweet = Conversation.tweets[tweet]
            datetimeLst['sentiment'].append(conv.sentiment)
            datetimeLst['length'].append(conv.length)
        df = pd.DataFrame(datetimeLst)
        binned = pd.cut(df['sentiment'], bin, labels=labels)
        df['sentiment'] = binned
        df = df.groupby('length')['sentiment'].value_counts().unstack().fillna(0)
        labels.reverse()
        df = df.loc[:,labels]
        df = df.loc[range(3,11), :]
        df["sum"] = df.sum(axis=1)
        df_new = df.loc[:,labels].div(df["sum"], axis=0)
        df_new.plot.bar(stacked=True, figsize=(10,7),xlim=list([2,10]), cmap='coolwarm')
        plt.title('Relative distribution of sentiment for length')
        plt.plot()
        plt.show()

    
lst = []
lst.append(None)
print(lst)
