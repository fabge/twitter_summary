import requests
from requests_oauthlib import OAuth1
import pickle
import os

API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

auth = OAuth1(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

url = 'https://api.twitter.com/1.1/statuses/home_timeline.json?count=200'

new_tweets = requests.get(url, auth=auth).json()

with open(r"tweet_collection.pickle", "rb") as input_file:
    tweet_collection = pickle.load(input_file)

for new_tweet in new_tweets:
    new = True
    for old_tweet in tweet_collection:
        if new_tweet['id'] == old_tweet['id']:
            new = False
    if new:    
        tweet_collection.append(new_tweet)
        
with open(r"tweet_collection.pickle", "wb") as output_file:
    pickle.dump(tweet_collection, output_file)