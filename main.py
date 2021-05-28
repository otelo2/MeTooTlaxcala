#!/usr/bin/python3
from TweetDownloader import TweetDownloader
from datetime import datetime

def main():
    tweetDownloader = TweetDownloader()
    if (tweetDownloader.newTweet()):
        amount = tweetDownloader.numOfTweetsToDownload()
        print(f'There are {amount} new tweets, starting download...')
        downloadImages = True
        tweetDownloader.processTweetsToFile(downloadImages, amount)
    else:
        print(f"No new tweets on {datetime.now()}. \nExiting the program.")


if __name__ == "__main__":
    main()
