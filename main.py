#!/usr/bin/python3
from TweetDownloader import TweetDownloader

def main():
    tweetDownloader = TweetDownloader()
    if (tweetDownloader.newTweet()):
        #amount = tweetDownloader.numOfTweetsToDownload()
        amount = 1000
        print(f'There are {amount} new tweets, starting download...')
        downloadImages = True
        tweetDownloader.processTweetsToFile(downloadImages, amount)
    else:
        print("No new tweets. \nExiting the program.")


if __name__ == "__main__":
    main()
