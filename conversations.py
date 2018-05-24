# -*- coding: utf-8 -*-
"""
Created on Tue May 22 15:47:09 2018

@author: 20166843
"""
import access


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

class Conversation:
    
    tweets = {}
    reply_ids = []
    
    def __init__(self, tweets = {}):
        self.length = 0
        self.tweets_lst = []
        if tweets != {}:
            Conversation.tweets = tweets


    def addTweetDict(tweet_id, user, text, time, lang, reply_user = '', reply_tweet = ''):
        Conversation.tweets[tweet_id] = Tweet(tweet_id, user, text, reply_user, reply_tweet, time)

    
    def addTweetConversation(self, tweet_id, end = True):
        if end:
            self.tweets_lst.append(tweet_id)
        else:
            self.tweets_lst = [tweet_id] + self.tweets_lst
        if Conversation.tweets[tweet_id].reply_tweet != '':
            tweet_id = Conversation.tweets[tweet_id].reply_tweet
            if tweet_id in Conversation.reply_ids:
                self.addTweetConversation(tweet_id)
            else:
                print(tweet_id)
                if self.getTweet(tweet_id):
                    self.addTweetConversation(tweet_id)
        tweet_id = self.tweets_lst[0]
        self.tweets_lst.reverse()
        len(self)
            
            
    def getTweet(self, tweetid):
        
        if tweetid in Conversation.tweets.keys():
            return Conversation.tweets[tweetid]
        else:
            q = """SELECT * FROM tweets WHERE tweet_id == {}""".format(tweetid)
            print(q)
            cursor = database.cursor()
            cursor.execute(q)
            try:
                tweet = cursor.fetchall()[0]
                database.commit()
                """id, date, user, text, replt tweet, reply user, lang"""
                Conversation.tweets[tweetid] = Tweet(tweet[0], tweet[2], tweet[3], 
                                    tweet[1], tweet[6], tweet[4], tweet[5])
                return True
            except:
                database.commit()
                return None
    
    
    def addTweets(user_id, user_name, start_date = '2016-02-01 00:00:00', end_date = '2017-06-01 00:00:00'):
        query = """SELECT * FROM tweets WHERE (user_id == {} OR 
            in_reply_to_user_id == {} OR text LIKE '%@{}%') AND
            datetime(created_at) >= datetime('{}') AND 
            datetime(created_at) < datetime('{}');""".format(user_id, user_id, user_name, start_date, end_date)
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
                              reply_tweet, reply_user)
    
    
    def replyIdList():
        query = """SELECT in_reply_to_tweet_id FROM tweets 
        WHERE in_reply_to_tweet_id NOT NULL;"""
        cursor = database.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        database.commit()
        Conversation.reply_ids = set([i[0] for i in result])
    
    
    def __len__(self):
        if self.tweets[0].reply_user != '' or self.tweets[0].reply_tweet != '':
            return len(self.tweets) + 1
        else:
            return len(self.tweets)
    
    
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
        self.time = time
    

Conversation.replyIdList()
print(len(Conversation.reply_ids))
Conversation.addTweets(user_id = '22536055',user_name= 'AmericanAir')

def makeConversations():
    for tweet_id in Conversation.tweets.keys():
        conversation = Conversation()
        if tweet_id in Conversation.reply_ids:
            continue
        conversation.addTweetConversation(tweet_id)
        if conversation.length > 1:
            conversationList.append(conversation)


makeConversations()

print(conversationList[10000].tweets_lst)




