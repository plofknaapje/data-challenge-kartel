# -*- coding: utf-8 -*-
"""
Created on Tue May 29 23:41:36 2018

@author: Twan
"""
import pickle

# 13 files
file_names = ["Conversations_AA.pkl", "Conversations_AirBerlin_Assist.pkl", 
              "Conversations_AirBerlin.pkl", "Conversations_AirFrance.pkl", 
              "Conversations_BA.pkl", "Conversations_EasyJet.pkl", 
              "Conversations_EtihadAirways.pkl", "Conversations_KLM.pkl", 
              "Conversations_Lufthansa.pkl", "Conversations_Qantas.pkl", 
              "Conversations_RyanAir.pkl", "Conversations_SingaporeAir.pkl", 
              "Conversations_VirginAtlantic.pkl"]

def open_conv_file(file_name):
    with open(file_name, 'rb') as f:
        if file_name == file_names[0]:
            global conv_AA
            conv_AA = pickle.load(f)
        elif file_name == file_names[2]:
            conv_AirBerlin = pickle.load(f)
        elif file_name == file_names[1]:
            global conv_AB_Assist
            conv_AB_Assist = pickle.load(f)
        elif file_name == file_names[3]:
            conv_AirFrance = pickle.load(f)
        elif file_name == file_names[4]:
            conv_BA = pickle.load(f)
        elif file_name == file_names[5]:
            conv_Easyjet = pickle.load(f)
        elif file_name == file_names[6]:
            conv_Etihad = pickle.load(f)
        elif file_name == file_names[7]:
            conv_KLM = pickle.load(f)
        elif file_name == file_names[8]:
            conv_Lufthansa = pickle.load(f)
        elif file_name == file_names[9]:
            conv_Qantas = pickle.load(f)
        elif file_name == file_names[10]:
            conv_RyanAir = pickle.load(f)
        elif file_name == file_names[11]:
            conv_SingaporeAir = pickle.load(f)
        elif file_name == file_names[12]:
            conv_Virgin = pickle.load(f)
with open("Conversations_AA.pkl", 'rb') as f:
    conv_AA = pickle.load(f)



for conversation in conversationList:
    for tweet in conversation.tweets_lst:
        Tweet = Conversation.tweets[tweet].text
        conv_sent = Conversation.tweets[tweet].text
        print(Tweet, conv_sent)
    print('!END OF CONVERSATION!')