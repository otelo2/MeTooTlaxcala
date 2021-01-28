import tweepy
import json
from keys import apiKey, apiSecret, accessToken, accessTokenSecret

auth = tweepy.OAuthHandler(apiKey, apiSecret)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth)

#Used for downloading the tweets from the account and storing them in a text file.
def downloadTweets():
    f = open("tweets.txt", "a", encoding="utf-8")

    #Gets the complete timeline without replies or retweets, and saves it on a text file.
    for tweet in tweepy.Cursor(api.user_timeline, id='MeToo_Tlx', exclude_replies=True, include_rts=False, tweet_mode='extended').items(3000):
        try:
            text = tweet.full_text
            text = text.replace('\n',' -- ')
            #print(text)
            #print('\n')
            f.write(text)
            f.write('\n')
        except UnicodeEncodeError:
            print("potential emoji found")

    f.close()

def setFileTemplate():
    f = open("tweets.txt", "w", encoding="utf-8")
    f.write("#Nombre    Apellido Paterno    Apellido Materno    Denuncia   Imagenes Fecha   Link")
    f.close()

def main():
    setFileTemplate()
    downloadTweets()

if __name__ == "__main__":
    main()

