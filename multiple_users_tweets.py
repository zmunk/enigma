import time
import json
import tweepy
from utils import *
from itertools import islice

# Twitter API
CONSUMER_KEY = AuthInfo.CONSUMER_KEY
CONSUMER_SECRET = AuthInfo.CONSUMER_SECRET
ACCESS_TOKEN = AuthInfo.ACCESS_TOKEN
ACCESS_TOKEN_SECRET = AuthInfo.ACCESS_TOKEN_SECRET

# JSON
INPUT_FILENAME = "eng_usernames.txt"
OUTPUT_FILENAME = "tweets.json"

def get_timeline_tweets(api, username):
    ''' retrieves ~3k tweets from specified user '''
    user_tweets = tweepy.Cursor(api.user_timeline, id=username, tweet_mode='extended')

    print(f"getting tweets for {username}")

    tweets = {}
    counter = 0
    start_time = time.time()
    try:
        for tweet in user_tweets.items():
            tweet_id = tweet.id_str
            full_text = tweet.full_text
            tweets[tweet_id] = full_text
            counter += 1
            if counter % 100 == 0:
                print(".", end="")
    except tweepy.error.TweepError:
        print("could not get tweet")
        return False
    except Exception as e:
        print(e)

    print(f"\nCollected {counter} tweets [{time.time() - start_time:.2f} s]")
    return tweets

def get_api():
    ''' setup tweepy auth '''
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    return tweepy.API(auth)

if __name__ == "__main__":  # main function
    sleep_duration = 10 # sec

    api = get_api()
    all_tweets = {}
    with open(INPUT_FILENAME) as file:
        for line in file:
            username = line.strip("\n")
            while True:
            # this loop allows the stream to reset after blocked by twitter API
                tweets = get_timeline_tweets(api, username)
                if tweets and len(tweets) > 0:
                    all_tweets[username] = tweets
                    break

                print(f"sleeping for {sleep_duration} seconds")
                time.sleep(sleep_duration)
                api = get_api() # reset api

    print(f"\nsaving users' tweets in {OUTPUT_FILENAME}\n")
    with open(OUTPUT_FILENAME, "w") as file:
        file.write(json.dumps(all_tweets))


        
    
    