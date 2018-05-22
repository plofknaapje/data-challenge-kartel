# -*- coding: utf-8 -*-
"""
Created on Tue May 22 15:47:09 2018

@author: 20166843
"""

class Conversation:
    
    tweets = []
    length = 0
        
    
    def addTweet(self, tweet_id, user, text, reply_user, reply_tweet, time):
        self.tweets.append(Tweet(tweet_id, user, text, reply_user, reply_tweet, time))
        self.length = self.__len__()
    
    
    def __len__(self):
        if self.tweets[0].reply_user != '' or self.tweets[0].reply_tweet != '':
            return len(self.tweets) + 1
        else:
            return len(self.tweets)
        

class Tweet:
    
    
    def __init__(self, tweet_id, user, text, time, reply_user = '', reply_tweet = ''):
        self.tweet_id = tweet_id
        self.user = user
        self.text = text
        self.reply_user = reply_user
        self.reply_tweet = reply_tweet
        self.time = time
    
    
conversationlist = []
conversationlist.append(Conversation)
    
    
testtweet = ['1234', '7000', 'AA is the best', '4000', '1233', '10:00']

conv = Conversation()
conv.addTweet(testtweet[0], testtweet[1], testtweet[2],  testtweet[5], testtweet[3], testtweet[4])
print(conv.length)


lst = [conv]
print(len(lst[0]))
conver = lst[0]
lst[0].addTweet('1233', '112', 'Blabla', '21:00', '', '')
print(len(conver))