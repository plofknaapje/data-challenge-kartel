# JBG030 Data Challenge Group 9
Project JBG030 Data Challenge for first year Data Science students

# Requirements
* An python environment which supports graphs in the console output like Spyder (https://github.com/spyder-ide/spyder)
* Python 3
* Python modules: datetime, seaborn, pandas, matplotlib, re, sqlite3, numpy and vaderSentiment
    * These modules can be installed using pip or conda

# Running the code
In order to run this code with new zipped json files, do the following:
1. Unzip the json files to the airlines_complete folder
2. Open this folder with Spyder or alike
2. Run access.py here. This creates the sqlite database with all the tweets in the data folder.
3. Run the file which contains the functions you want:
    a. Conversations.py for sentiment analysis, heatmaps and sentiment distribution 
    
# access.py


# conversations.py

# sentiment_airlines.py
This code executes sentiment analysis with the vaderSentiment module.
It saves two .CSV files
1. sentiment_airlines.csv with the compound sentiment score for every airline.
2. Labeled_sentiment.csv with the sentiment scores labeled by text representative of the sentiment score.

# Sentiment_distribution_plot
This code counts the number of (slightly/very)positive/(slightly/very)negative/neutral tweets per airlines.
After this the numbers are put in a stacked bar chart (by hand).
This creates a nice overview of the distribution of the sentiment.

# Sentiment lexicon
This code creates lexicons of words which appear in positive/negative tweets.
This is done by using dictionaries and with keys as words (in tweets) and values as the number of time a certain word appears.








