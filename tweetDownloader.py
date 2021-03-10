import tweepy
import json
import os
from keys import apiKey, apiSecret, accessToken, accessTokenSecret

auth = tweepy.OAuthHandler(apiKey, apiSecret)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth)


#Sets the template for the text file
def setFileTemplate():
    f = open("tweets.txt", "w", encoding="utf-8")
    f.write("#Nombre    Apellido Paterno    Apellido Materno    Denuncia   Imagenes Fecha   Link \n")
    f.close()


#Used for downloading the tweets from the account, processing them and storing them in a text file.
#No terminal output (except for wget maybe)
def processTweetsToFile(images=True, numOfTweets=3000):
    #Open the file where the tweets are stored
    f = open("tweets.txt", 'a', encoding="utf-8")
    
    tweets = []
    for tweet in tweepy.Cursor(api.user_timeline, id='MeToo_Tlx', exclude_replies=True, include_rts=False, tweet_mode='extended').items(numOfTweets):
        tweets.append(tweet)

    for tweet in reversed(tweets):
        #Clear the output for the text file
        textForFile = ''

        #Name of the person
        nombre = findName(tweet.full_text)
        textForFile += nombre + "    "

        #Text of the tweet
        denuncia = tweet.full_text
        textForFile += denuncia + "    "

        #Images of the tweet
        if "media" in tweet.entities:
            for media in tweet.extended_entities['media']:
                #print(len(tweet.extended_entities['media']))
                url = media['media_url']
                #Download images (or not)
                if images == True:
                    imgDirectory = downloadImages(nombre, url)
                    textForFile += imgDirectory + "    "

        #Time and date of the tweet
        fecha = str(tweet.created_at)
        textForFile += fecha + "    "

        #Url of the tweet
        url = "https://twitter.com/twitter/statuses/" + str(tweet.id)
        textForFile += url + "    "
        textForFile += str(tweet.id) + "    "

        #Write the info to the text file
        f.write(textForFile + "\n")
    f.close()


def findName(text):
    #Refresh Output
    fullName = ""

    #Open the list of names
    nameFile = open("nombresMasculinos.txt", 'r', encoding='utf-8')
    nameSet = set(line.strip() for line in nameFile)
    nameFile.close()

    #Text in which we search for names
    #Convert the string into a list
    textList = text.split()

    #See if there is a match with our list of namaes
    try:
        #Use set operations to see if words match the list (here set) of names. If there isn't the exeption is raised.
        match = set(textList) & nameSet

        #Prepare the found names to be iterated
        nameList = list(match)
        nameList.sort()

        #Go trough every name found
        for nombre in (nameList):
            index = textList.index(nombre)
            fullName += nombre + " "
            #Try to print surnames.
            #There is a chance of printing things other than the surnames. To fix it I'd need a list of surnames for there are way more surnames than names
            #Of course, we asume that the surnames will come after the name and that there will be 2 surnames. This may need changing.
            try:
                #Paternal surname
                fullName += str(textList[index+1]) + " "
                #Maternal surname
                fullName += str(textList[index+2]) + " -- "
            except IndexError:
                print("Index error")
    except ValueError:
        print("Name not found in the text")
    
    return fullName


#Use wget to download the images from Twitter
def downloadImages(person, url):
    filename = person+url[-7]
    filename = filename.replace(" ", "")
    downloadCommand = "cd img && wget -O \""+filename+".jpg\" " +url
    os.system(downloadCommand)
    return "/img/"+filename+".jpg"


#Checks if the last stored tweet in the file is the latest tweet
def newTweet():
    #Find ID of the most recent tweet in the file
    with open('tweets.txt', 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()
        try:
            last_line = lines[-1]
            last_line = last_line.split()
            latestFileID = last_line[-1]
        except IndexError:
            return True

    #Find ID of the latest tweet in Twitter
    for tweet in tweepy.Cursor(api.user_timeline, id='MeToo_Tlx', exclude_replies=True, include_rts=False, tweet_mode='extended').items(1):
        latestID = tweet.id
    
    #Check if they are the same
    if (int(latestFileID) == latestID):
        #print("We already have the latest tweet. ", latestFileID, latestID)
        return False
    else:
        #print("We don't have the latest tweet.", latestFileID, latestID)
        return True


#Checks how up to date is our data and update if we are missing tweets.Tells how many tweets we are missing.
def numOfTweetsToDownload():
    latestID=-1
    check=1
    tweets=0

    #Find ID of the most recent tweet in the file
    with open('tweets.txt', 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()
        try:
            last_line = lines[-1]
            last_line = last_line.split()
            latestFileID = last_line[-1]
        except IndexError:
            return 3000

    #Find ID of the most recent tweet in Twitter
    for tweet in tweepy.Cursor(api.user_timeline, id='MeToo_Tlx', exclude_replies=True, include_rts=False, tweet_mode='extended').items(check):
        latestID = tweet.id

    if int(latestFileID) != latestID:
        #We have to download at least one, check how many more we have to download
        #While we dont have the latest tweet, count how many we have to download
        while int(latestFileID) != latestID:
            #Find ID of the latest tweet in Twitter
            for tweet in tweepy.Cursor(api.user_timeline, id='MeToo_Tlx', exclude_replies=True, include_rts=False, tweet_mode='extended').items(check):
                latestID = tweet.id
            
            check = check + 1
            tweets = tweets + 1

        tweets = tweets - 1
        #print("You have to download", tweets)
        return tweets



def main():
    if (newTweet()):
        amount = numOfTweetsToDownload()
        print(f'There are {amount} new tweets, starting download...')
        downloadImages = True
        processTweetsToFile(downloadImages, amount)
    else:
        print("No new tweets. \nExiting the program.")


if __name__ == "__main__":
    main()
