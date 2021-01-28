import tweepy
import json
from keys import apiKey, apiSecret, accessToken, accessTokenSecret

auth = tweepy.OAuthHandler(apiKey, apiSecret)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth)

f = open("tweets.txt", "w", encoding="utf-8")

for tweet in tweepy.Cursor(api.user_timeline, id='MeToo_Tlx', exclude_replies=True, include_rts=False, tweet_mode='extended').items(3000):
    try:
        text = tweet.full_text
        text = text.replace('\n',' -- ')
        print(text)
        print('\n')
        f.write(text)
        f.write('\n')
    except UnicodeEncodeError:
        print("potential emoji found")

f.close()
