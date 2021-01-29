import tweepy
import json
from keys import apiKey, apiSecret, accessToken, accessTokenSecret

auth = tweepy.OAuthHandler(apiKey, apiSecret)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth)

#Sets the template for the text file
def setFileTemplate():
    f = open("tweets.txt", "w", encoding="utf-8")
    f.write("#Nombre    Apellido Paterno    Apellido Materno    Denuncia   Imagenes Fecha   Link")
    f.close()

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

#Testing function
def test():
    for tweet in tweepy.Cursor(api.user_timeline, id='MeToo_Tlx', exclude_replies=True, include_rts=False, tweet_mode='extended').items(1):
        #Name of the person
        print("Nombre: ", findName(tweet.full_text))

        #Text of the tweet
        print("Denuncia: " + tweet.full_text)

        #Images of the tweet
        if "media" in tweet.entities:
            for media in tweet.extended_entities['media']:
                print("Imagen: " + media['media_url'])

        #Time and date of the tweet
        print("Fecha: " + str(tweet.created_at))

        #Url of the tweet
        url = "https://twitter.com/twitter/statuses/" + str(tweet.id)
        print("Link: " + url)

        print('\n')

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

def main():
    #print("a")
    print("Nombre: ", findName('Carlos Sarmiento Tuxpan de San Lorenzo Axocomanitl'))

if __name__ == "__main__":
    main()

