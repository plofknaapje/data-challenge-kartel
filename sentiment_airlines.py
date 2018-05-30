# -*- coding: utf-8 -*-
"""
Created on Wed May 30 14:55:46 2018

@author: Vincent_Vast
"""

# -*- coding: utf-8 -*-
"""
Created on Tue May 22 15:47:09 2018

@author: 20166843
"""
import access
from textblob import TextBlob
import re
import pickle
from datetime import datetime, timedelta
import seaborn as sns; sns.set()
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
import numpy as np



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
counterair = 0
dfairlines = pd.DataFrame()
for airline in airlines_names:
    dfprop = pd.DataFrame()
# Default for AA
    user_id = airlines_id[counterair]
    user_name = airlines_names[counterair]
    
    
    class Conversation:
        
        '''
        Class which contains a class dictionary with all relevant tweets as Tweet
        objects.
        Also contains a list with all tweets to which was replied.
        '''
       
        tweets = {}
        reply_ids = []
       
        def __init__(self, tweets = {}):
            '''
            Initializes basic variables of the object.
            :param tweets: optional dictionary to skip the building of the dict.
            '''
            self.length = 0
            self.tweets_lst = []
            if tweets != {}:
                Conversation.tweets = tweets
     
        
        def setup(user_id, user_name):
            Conversation.user_id = user_id
            Conversation.user_name = user_name
        
     
    
        def addTweetDict(tweet_id, user, text, time, lang, reply_user = '', reply_tweet = ''):
            Conversation.tweets[tweet_id] = Tweet(tweet_id, user, text, time, lang, reply_user, reply_tweet)
    
        def addTweetConversation(self, tweet_id, end = False):
            tweet = Conversation.tweets[tweet_id]
            if end:
                self.tweets_lst.append(tweet_id)
            else:
                self.tweets_lst = [tweet_id] + self.tweets_lst
           
            tweet_id = tweet.reply_tweet
            if tweet.reply_tweet in Conversation.tweets.keys():
                self.addTweetConversation(tweet_id)
            elif tweet_id != None:
                if self.getTweet(tweet_id):
                    self.addTweetConversation(tweet_id)
                   
            self.length = len(self)
    
        def getTweet(self, tweetid):
           
            if tweetid in Conversation.tweets.keys():
                return Conversation.tweets[tweetid]
            else:
                q = """SELECT * FROM tweets WHERE tweet_id == {}""".format(tweetid)
                cursor = database.cursor()
               
                try:
                    cursor.execute(q)
                    tweet = cursor.fetchall()[0]
                    database.commit()
                    """id, date, user, text, replt tweet, reply user, lang"""
                    Conversation.tweets[tweetid] = Tweet(tweet[0], tweet[2], tweet[3],
                                        tweet[1], tweet[6], tweet[4], tweet[5])
                    return True
                except:
                    database.commit()
                    return None
       
       
        def addTweets(start_date = '2016-02-01 00:00:00', end_date = '2017-06-01 00:00:00'):
    
            query = """SELECT * FROM tweets WHERE (user_id == {} OR
                in_reply_to_user_id == {} OR text LIKE '%@{}%') AND
                datetime(created_at) >= datetime('{}') AND
                datetime(created_at) < datetime('{}');""".format(Conversation.user_id, 
                Conversation.user_id, Conversation.user_name, start_date, end_date)
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
                Conversation.addTweetDict(tweet_id, user, text, created, lang,
                                  reply_user, reply_tweet)
    
        def replyIdList():
            query = """SELECT in_reply_to_tweet_id FROM tweets
            WHERE in_reply_to_tweet_id NOT NULL;"""
            cursor = database.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            database.commit()
            Conversation.reply_ids = set([i[0] for i in result if i != 'None'])
            
        
        def containsUser(self):
            self.startingDate()
            contains = False
            for tweet in self.tweets_lst:
                tweet = Conversation.tweets[tweet]
                if tweet.user == Conversation.user_id:
                    contains = True
            return contains
       
        
        def startingDate(self):
            self.time = datetime.strptime('2017-06-01 00:00:00', '%Y-%m-%d %H:%M:%S')
            for tweet in self.tweets_lst:
                tweet = Conversation.tweets[tweet]
                if tweet.time < self.time:
                    self.time = tweet.time
                
    
        def __len__(self):
            if True:
                return len(self.tweets_lst)
            tweet = Conversation.tweets[self.tweets_lst[0]]
            if tweet.reply_tweet != '':
                return len(self.tweets_lst) + 1
            elif tweet.user in airlines_id and tweet.reply_user != None:
                return len(self.tweets_lst) + 1
            else:
                return len(self.tweets_lst)
    
        def __return__(self):
            return [Conversation.tweets[tweet] for tweet in self.tweets_lst]
           
     
    class Tweet:
       
        def __init__(self, tweet_id, user, text, time, lang, reply_user = '', reply_tweet = ''):
            self.tweet_id = tweet_id
            self.user = user
            self.text = text
            self.lang = lang
            self.reply_user = reply_user
            self.reply_tweet = reply_tweet
            self.time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S+00:00')
       
        def __str__(self):
            return 'ID:{} user:{} text:{} lang:{} reply_user:{} reply_tweet:{} created:{}'.format(self.tweet_id,
                       self.user, self.text, self.lang, self.reply_user, self.reply_tweet, self.time)
     
    def listToDict(lst):
        dicti = {}
        for i in lst:
            if str(i) in dicti.keys():
                dicti[str(i)] = dicti[str(i)] + 1
            else:
                dicti[str(i)] = 1
        return dicti
     
    def makeConversations(user_id, user_name):
        Conversation.setup(user_id, user_name)
        Conversation.replyIdList()
        Conversation.addTweets()
    
        for tweet_id in list(Conversation.tweets.keys()):
            if not tweet_id in Conversation.reply_ids:
                conversation = Conversation()
                conversation.addTweetConversation(tweet_id)
                if conversation.length > 1 and conversation.containsUser():
                    conversationList.append(conversation)
        times = [len(conv) for conv in conversationList]
        return listToDict(times)
    
    
    if __name__ == "__main__":
        # execute only if run as a script
        
        dicti = makeConversations(user_id, user_name)
        
        datetimeLst = {'hour':[], 'length':[], 'date':[]}
        for conv in conversationList:
            dt = conv.time
            if user_name == 'AmericanAir':
                dt = dt - timedelta(hours=6)
            datetimeLst['hour'].append(dt.hour)
            datetimeLst['date'].append(dt.strftime('%Y-%m-%d'))
            datetimeLst['length'].append(conv.length)
            
        df = pd.DataFrame(datetimeLst)
        amount_results = df.groupby(['date','hour']).size().reset_index().rename(columns={0:'count'})
        amount_results['date'] = pd.to_datetime(amount_results['date'],format='%Y-%m-%d')
        amount_results['day'] = amount_results['date'].dt.weekday
        amount_results.drop(['date'], axis=1)
        amount_results = amount_results.groupby(['day', 'hour']).mean().reset_index()
        amount_results = amount_results.pivot('hour', 'day', 'count')
        
        ax = sns.heatmap(amount_results, cmap='Blues')
        ax.invert_yaxis()
        ax
        plt.xlabel("day of the week")
        plt.xticks([0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5], ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
        plt.ylabel("hour of the day")
        plt.yticks([0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 11.5, 12.5,
                13.5, 14.5, 15.5, 16.5, 17.5, 18.5, 19.5, 20.5, 21.5, 22.5, 23.5],
               ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00",
                "07:00", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00",
                "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00",
                "21:00", "22:00", "23:00"], rotation=0)
        plt.title('Average amount of conversation with {}'.format(user_name))
        plt.plot()
        # times = [len(conv) for conv in conversationList]
        
        
        '''
        dicti = listToDict(times)
        print(dicti)
        '''
    
    
     
    def processTweet(tweet):
        # process the tweets
     
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
    
    """tweet_ids_lst = []
    tweet_text_lst = []
    tweet_sentiment_score = []
    counter = 0
    for key in Conversation.tweets.keys():
        if Conversation.tweets[key].user != user_id
        tweet_ids_lst.append(key)
    
        proctweet = processTweet(Conversation.tweets[key].text)
        tweet_text_lst.append(proctweet)
    
        blob = TextBlob(proctweet)
        tweet_sentiment_score.append(blob.sentiment.polarity)
        print(counter)
        counter += 1
        """
    
    
    """for i in range(len(tweet_ids_lst)):
        Conversation.tweets[tweet_ids_lst[i]].sentiment = tweet_sentiment_score[i]
    for conversation in conversationList:
        for tweet in conversation.tweets_lst:
            Tweet = Conversation.tweets[tweet].text
            conv_sent = Conversation.tweets[tweet].text
            print(Tweet, conv_sent)
        print('!END OF CONVERSATION!')"""
    
    
    """with open('Conversations_VirginAtlantic.pkl', 'wb') as f:
        pickle.dump(conversationList, f)"""
    
   
    
    
    tweet_ids_lst = []
    tweet_text_lst = []
    
    tweet_sentiment_score = []
    counter = 0
    
    counterair += 1
    for key in Conversation.tweets.keys():
        if Conversation.tweets[key].user != user_id:
            tweet_ids_lst.append(key)
       
            proctweet = processTweet(Conversation.tweets[key].text)
            tweet_text_lst.append(proctweet)
       
            blob = TextBlob(proctweet)
           
            tweet_sentiment_score.append(blob.sentiment.polarity)
            print(counter)
            counter += 1
    dfprop[airline] = tweet_sentiment_score
    dfairlines = pd.concat([dfairlines, dfprop], axis=1)

dfairlines.head()
dfairlines.to_csv('sentiment_airlines.csv')
dfairlines


df_sentiment = pd.DataFrame()
bin = [-1, -0.75, -0.25, -0.000001, 0.000001, 0.25, 0.75, 1]
labels = ['Very negative', 'Negative', 'Slightly negative', 'Neutral', 'Slightly positive', 'Positive', 'Very positive']
df12 = pd.read_csv('sentiment_airlines.csv')
for airline in airlines_names:
    category = pd.cut(df12[airline], bin, labels = labels)
    df_sentiment[airline] = category.to_frame()
df_sentiment.to_csv('labeled_sentiment.csv')

