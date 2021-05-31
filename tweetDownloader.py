#!/usr/bin/python3
import tweepy
import requests
import shutil
from keys import apiKey, apiSecret, accessToken, accessTokenSecret

#Constructor
auth = tweepy.OAuthHandler(apiKey, apiSecret)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth)
class TweetDownloader:
    

    #Sets the template for the text file
    def setFileTemplate(self):
        f = open("tweets.txt", "w", encoding="utf-8")
        f.write("#Nombre    Apellido Paterno    Apellido Materno    Denuncia   Imagenes Fecha   Link \n")
        f.close()

    #Used for downloading the tweets from the account, processing them and storing them in a text file.
    #No terminal output except for wget 
    def processTweetsToFile(self, images=True, numOfTweets=1000):
        #Open the file where the tweets are stored
        f = open("tweets.txt", 'a', encoding="utf-8")
        
        tweets = []
        for tweet in tweepy.Cursor(api.user_timeline, id='MeToo_Tlx', exclude_replies=True, include_rts=False, tweet_mode='extended').items(numOfTweets):
            tweets.append(tweet)

        for tweet in reversed(tweets):
            #Name of the person
            nombre = self.findName(tweet.full_text)

            #Text of the tweet
            denuncia = tweet.full_text
            #Remove commas so there isn't problems when splitting the file
            denuncia = denuncia.replace(",","")

            #Images of the tweet
            imgDirectory = ""
            if "media" in tweet.entities:
                for media in tweet.extended_entities['media']:
                    #print(len(tweet.extended_entities['media']))
                    url = media['media_url']
                    #Download images (or not)
                    if images == True:
                        #downloadImages regresa el nombre del archivo
                        imgDirectory += f"{self.downloadImages(nombre, url)}, "

            #Time and date of the tweet
            date = str(tweet.created_at)
            date = date.split(" ")
            fecha = date[0]
            hora = date[1]

            #Url of the tweet
            url = "https://twitter.com/twitter/statuses/" + str(tweet.id)

            #Write the info to the text file
            textForFile = f"{nombre}, {denuncia}, {imgDirectory}, {fecha}, {hora}, {url}, {str(tweet.id)}\n"
            f.write(textForFile)
        f.close()


    #Identifies a name inside a text.
    #Used to find and get the name(s?) found in a tweet
    def findName(self, text):
        #Refresh Output
        fullName = ""

        #Open the list of names
        nameFile = open("nombresMasculinos.txt", 'r', encoding='utf-8')
        nameSet = set(line.strip() for line in nameFile)
        nameFile.close()

        #Text in which we search for names
        #Remove commas, dots, "", /
        text = text.replace(",","")
        text = text.replace(".","")
        text = text.replace("\"","")
        text = text.replace("/","")
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
    def downloadImages(self, person, url):
        #Set the filename as the persons name
        #Adding some symbols so images dont overwrite
        filename = person+url[-7]+url[-6]+url[-5]

        #Remove the spaces of the name
        filename = filename.replace(" ", "")

        #Get the content of the image from the url
        req = requests.get(url, stream=True)

        #If image retrieval was successful
        if req.status_code == 200:
            #So the image has a size
            req.raw.decode_content = True

            #Save image to the img directory. 
            with open('img/'+filename, 'wb') as f:
                shutil.copyfileobj(req.raw, f)

            #Sucess maybe.
            print("Saved image to: img/"+filename)

            #Return the path to the image
            return "/img/"+filename+".jpg"
        else:
            print("There was an error getting the image. "+req.status_code)


    #Checks if the last stored tweet in the file is the latest tweet
    def newTweet(self):
        #Find ID of the most recent tweet in the file
        try:
            with open('tweets.txt', 'r', encoding='utf-8') as f:
                lines = f.read().splitlines()
                try:
                    last_line = lines[-1]
                    last_line = last_line.split()
                    latestFileID = last_line[-1]
                except IndexError:
                    return True
        except FileNotFoundError:
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
    def numOfTweetsToDownload(self):
        latestID=-1
        check=1
        tweets=0

        #Find ID of the most recent tweet in the file
        try:
            with open('tweets.txt', 'r', encoding='utf-8') as f:
                lines = f.read().splitlines()
                try:
                    last_line = lines[-1]
                    last_line = last_line.split()
                    latestFileID = last_line[-1]
                except IndexError:
                    return 1000
        except FileNotFoundError:
            return 1000

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
