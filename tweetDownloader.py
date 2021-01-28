import tweepy
import json
from keys import apiKey, apiSecret, accessToken, accessTokenSecret

auth = tweepy.OAuthHandler(apiKey, apiSecret)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth)

f = open("tweets.txt", "w")

for tweet in tweepy.Cursor(api.user_timeline, id='MeToo_Tlx', count='3000', exclude_replies=True, include_rts=False).items(3000):
    print(tweet.text)
    print('\n')
    f.write(tweet.text)
    f.write('\n')

f.close()
