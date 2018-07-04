# JBG030 Data Challenge Group 9
Project JBG030 Data Challenge for first year Data Science students

## Requirements
* An python environment which supports graphs in the console output like Spyder (https://github.com/spyder-ide/spyder)
* Python 3
* Python modules: datetime, seaborn, pandas, matplotlib, re, sqlite3, numpy and vaderSentiment
    * These modules can be installed using pip or conda
* RStudio

## Running the code
In order to run this code with new zipped json files, do the following:
1. Unzip the json files to the airlines_complete folder
2. Open this folder with Spyder or alike
2. Run access.py here. This creates the sqlite database with all the tweets in the data folder.
3. Run the file which contains the functions you want:

### conversations.py
This file creates the class structure used in the rest of the project.
The airlineid variable should be set to the twitter id of interest.
It executes sentiment analysis on all tweets in order to measure the results of tweets by an airline.
It also creates two date-time heatmaps, one with the amount of conversations and another with the amount of unanswered tweets.
After this, it creates a stacked barchart which shows the distribution of the effect of airline tweets.

### sentiment_airlines.py
This file executes sentiment analysis with the vaderSentiment module.
It saves two .CSV files
1. sentiment_airlines.csv with the compound sentiment score for every airline.
2. Labeled_sentiment.csv with the sentiment scores labeled by text representative of the sentiment score.

### Sentiment_distribution_plot.py
This file uses the input "Labeled_sentiment.csv" as data. 
It also counts the number of (slightly/very)positive/(slightly/very)negative/neutral tweets per airlines.
After this the numbers are put in a stacked bar chart (by hand).
This creates a nice overview of the distribution of the sentiment.

### AA_sentiment_to_csv_for_lexicon.py
This file creates a csv with the sentiment score and tweet text from tweets to AA.
This CSV is used in the Sentiment_Lexicon.py

### Sentiment_Lexicon.py
This file uses sentiment_AA.csv as data which consists of all tweets to American Airlines with the tweet_text and sentiment per tweet.
This CSV is created by AA_sentiment_to_csv_for_lexicon.py
From that csv, this file creates lexicons of words which appear in positive and negative tweets.
This is done by using dictionaries  with keys as words (in tweets) and values as the number of time a certain word appears in the negative or positive tweets.
The tweets that are analyzed are incoming tweets from American Airlines.

### volume.py
This file creates 2 heatmaps: 1 for incoming volume and 1 for outgoing volume (sorted by date)

### location_sentiment.py
This file makes a gmap from the longitude, latitude from the incoming volume of American Airlines. 
The heat on the gmap stands for the sentiment with the greener the higher the sentiment.

## Statistical Tests
To run the statistical test, R was used. To repeat the tests, the following file can be run.

### Sentiment_Statistical_Test.R
This code conducts a ones-sided one-sample student t-test, to change whether there is a significant increase 
of sentiment on Twitter users after intervention by American Airlines. Note: The second row should be runned 
in conversations.py to create the csv file to be used in R.


