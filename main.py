#!/usr/bin/python3
import psycopg2
from DatabaseConnector import DatabaseConnector
from TweetDownloader import TweetDownloader
from datetime import datetime

def main():
    #Create objects for the classes
    tweetDownloader = TweetDownloader()
    databaseConnector = DatabaseConnector()

    #Create the database
    try:
        databaseConnector.createTable();
        print("Database not found. Creating...")
    except psycopg2.errors.DuplicateTable:
        print("Database already exists")
        pass

    #Check if there have been new tweets
    if (tweetDownloader.newTweet()):
        #Check how many new tweets there are
        amount = tweetDownloader.numOfTweetsToDownload()
        print(f'There are {amount} new tweets, starting download...')
        
        #Downloads the specified amount of tweets with images
        tweetDownloader.processTweetsToFile(True, amount)
        
        #Adds the specified amount of tweets to the database
        databaseConnector.specificTweetsFileToDatabase(True, amount)
        
        #Exports the whole databasase to a json file in Frontend/data
        databaseConnector.databaseToJSON()
    else:
        print(f"No new tweets on {datetime.now()}.")
        #print("If you have modified the tweets.txt file you have to update the data on the frontend.")
        #option = input("Do you want to do that now? (y/n) ").lower()
        #databaseConnector.databaseToJSON() if option == 'y' else exit()


if __name__ == "__main__":
    main()
