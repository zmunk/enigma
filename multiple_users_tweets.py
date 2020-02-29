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
INPUT_FILENAME = "out/eng_usernames.txt"
# OUTPUT_FILENAME = "out/multiple_user_tweets_test.json"


def get_timeline_tweets(api, username):
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

if __name__ == "__main__":

    # final_user = None
    left_off_line = 114 # 65
    file_counter = 17

    while True:
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)
        with open(INPUT_FILENAME) as in_f:

            if left_off_line:
                for _ in range(left_off_line - 1):
                    in_f.readline()
                current_line = left_off_line - 1
            else:
                current_line = -1

            all_tweets = {}

            for line in in_f:
                current_line += 1
                username = line.strip("\n")
                tweets = get_timeline_tweets(api, username)
                if tweets is False:
                    left_off_line = current_line
                    print(f"stopped at {username}, {left_off_line}")
                    break
                elif len(tweets) > 0:
                    all_tweets[username] = tweets

        if len(all_tweets) > 0:
            print(f"\nsaving users' tweets in tweets{file_counter}.json\n")
            with open(f"out/tweets/tweets{file_counter}.json", "w") as out_f:
                out_f.write(json.dumps(all_tweets))
            file_counter += 1
        else:
            break

        sleep_duration = 240 # sec
        print(f"sleeping for {sleep_duration} seconds")
        time.sleep(sleep_duration) # maximum 240 seconds
    
    