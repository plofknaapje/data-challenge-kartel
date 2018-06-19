### Needed libraries ###
import json
import glob
import sqlite3
from datetime import datetime



### Variables and constants ###
files = "airlines_complete"
test_file = "airlines_complete/airlines-1464602228450.json"

db = sqlite3.connect('data/mydb.sqlite3')
db1 = sqlite3.connect('data/myd.sqlite3')
cursor = db1.cursor()

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
    Complexity: O(n)
    :param directory: str of file with the json files.
    :return list:
    """
    return list(set(glob.glob(directory + "/*.json")))

def open_json_twitter(file_path):
    """
    Returns a list of directories which each represent a tweet.
    Complexity: O(n)
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
    Complexity: O(n)
    :param file_name: String of file location
    :param db: SQLite database connection object
    :param add_attributes: List with additional attributes
    :return: Success if succesful
    """
    for tweet in open_json_twitter(file_name): # O(n)
        if 'id_str' not in tweet.keys(): # O(1)
            continue
        created_at = datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S %z %Y')
        try: # O(1)
            test = tweet['lang']
        except KeyError:
            tweet['lang'] = 'und'
            
        long = None
        lati = None
        if tweet['coordinates'] != None: # O(1)
            long = tweet['coordinates']['coordinates'][0]
            lati = tweet['coordinates']['coordinates'][1]

        tweet_msg = [tweet['id_str'], created_at, tweet['user']['id_str'], tweet['text'],
                tweet['in_reply_to_status_id_str'], tweet['in_reply_to_user_id_str'], 
                tweet['lang'], long, lati]

        local_cursor = db.cursor()
        try: # O(1)
            local_cursor.execute('''INSERT INTO tweets(tweet_id, created_at, user_id, text, in_reply_to_tweet_id, 
                                    in_reply_to_user_id, lang, longitude, latitude) VALUES(?,?,?,?,?,?,?,?,?)''',tweet_msg)
            db.commit()
        except sqlite3.IntegrityError:
            continue
    return 'Success'

def build_database(db, directory = files):
    """
    Uploads the content of all json files in directory to the tweets table in the db.
    Complexity: O(mn)
    :param db: SQlite database connection object
    :param directory: str name of folder
    :return: Success if succesful
    """
    i = 1
    for file in file_list(directory): # O(n)
        db_upload(file, db) # O(m)
        print(350 - i)
        i = i + 1
    return 'Success'

if __name__ == "__main__":
    build_database(db1)