#!/usr/bin/python3
from DatabaseConnector import DatabaseConnector
from TweetDownloader import TweetDownloader
from datetime import datetime

def main():
    #Create objects for the classes
    tweetDownloader = TweetDownloader()
    databaseConnector = DatabaseConnector()
    #Check if there have been new tweets
    if (tweetDownloader.newTweet()):
        #Check how many new tweets there are
        amount = tweetDownloader.numOfTweetsToDownload()
        print(f'There are {amount} new tweets, starting download...')
        #Downloads the specified amount of tweets with images
        tweetDownloader.processTweetsToFile(True, amount)
        #Adds the specified amount of tweets to the database
        databaseConnector.specificTweetsFileToDatabase(True, amount)
    else:
        print(f"No new tweets on {datetime.now()}. \nExiting the program.")


if __name__ == "__main__":
    main()
