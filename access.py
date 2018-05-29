### Needed libraries ###
import json
import glob
import sqlite3
from datetime import datetime



### Variables and constants ###
files = "airlines_complete"
test_file = "airlines_complete/airlines-1464602228450.json"

db = sqlite3.connect('data/myd.sqlite3')
cursor = db.cursor()

try:
    cursor.execute('''
    CREATE TABLE tweets(tweet_id TEXT PRIMARY KEY, created_at TEXT,
                       user_id TEXT, text TEXT, in_reply_to_tweet_id TEXT, 
                       in_reply_to_user_id TEXT, lang TEXT, longitude FLOAT(24),
                       latitude FLOAT(24))
    ''')
    db.commit()
except sqlite3.OperationalError:
    db_exists = True


### Functions ###
def file_list(directory = "airlines_complete"):
    """
    Returns a list of unique json files in directory with the directory name added

    :param directory: str of file with the json files.
    :return list:
    """
    return list(set(glob.glob(directory + "/*.json")))

def open_json_twitter(file_path):
    """
    Returns a list of directories which each represent a tweet.

    :param file_path: String of file location
    :return: list of directories
    """
    tweets = []
    f = open(file_path, 'r')
    for line in f.readlines():
        try:
            tweet = json.loads(line)  # load it as Python dict
            tweets = tweets + [tweet]
        except:
            continue
    # print(json.dumps(tweets[0], indent=4))  # pretty-print
    f.close()
    return tweets

def db_upload(file_name, db):
    """
    Takes a string of the location of a json file.
    Uploads all the tweets to the mongoDB collection and ignore all other rows with the following attributes:
    _id as str, created_at as datetime, user_id as str, user_location as str, user_lang as str, text as str,
    in_reply_to_status_id_str as str, in_reply_to_user_id_str as str, lang as str.

    :param file_name: String of file location
    :param db: SQLite database connection object
    :param add_attributes: List with additional attributes
    :return: Success if succesful
    """
    for tweet in open_json_twitter(file_name):
        if 'id_str' not in tweet.keys():
            continue
        created_at = datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S %z %Y')
        try:
            test = tweet['lang']
        except KeyError:
            tweet['lang'] = 'und'
            
        long = None
        lati = None
        if tweet['coordinates'] != None:
            long = tweet['coordinates']['coordinates'][0]
            lati = tweet['coordinates']['coordinates'][1]

        tweet_msg = [tweet['id_str'], created_at, tweet['user']['id_str'], tweet['text'],
                tweet['in_reply_to_status_id_str'], tweet['in_reply_to_user_id_str'], 
                tweet['lang'], long, lati]

        local_cursor = db.cursor()
        try:
            local_cursor.execute('''INSERT INTO tweets(tweet_id, created_at, user_id, text, in_reply_to_tweet_id, 
                                    in_reply_to_user_id, lang, longitude, latitude) VALUES(?,?,?,?,?,?,?,?,?)''',tweet_msg)
            db.commit()
        except sqlite3.IntegrityError:
            continue
    return 'Success'

def build_database(db, directory = files):
    """
    Uploads the content of all json files in directory to the tweets table in the db.
    :param db: SQlite database connection object
    :param directory: str name of folder
    :return: Success if succesful
    """
    i = 1
    for file in file_list(directory):
        db_upload(file, db)
        print(350 - i)
        i = i + 1
    return 'Success'

build_database(db)