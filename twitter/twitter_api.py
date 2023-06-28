import os
import requests
import json
import datetime
import pandas as pd
import snscrape.modules.twitter as sntwitter

from dotenv import load_dotenv
from pathlib import Path

class TwitterAPI:

    def __init__(self):

        # Load environment variables from .env file
        env_path = Path('..') / '.env'
        load_dotenv(dotenv_path=env_path)

        # Twitter tokens
        self._TWITTER_API_KEY = os.environ['TWITTER_API_KEY']
        self._TWITTER_API_KEY_SECRET = os.environ['TWITTER_API_KEY_SECRET']
        self._TWITTER_ACCESS_TOKEN = os.environ['TWITTER_ACCESS_TOKEN']
        self._TWITTER_ACCESS_TOKEN_SECRET = os.environ['TWITTER_ACCESS_TOKEN_SECRET']
        self._TWITTER_BEARER_TOKEN = os.environ['TWITTER_BEARER_TOKEN']

        self.username_file_path = './username_list.txt'
        self.usernames = []
        self.NUMBER_OF_SCRAPED_TWEETS = 5
        self.df = None 

    # Reads the latest list of usernames from username_list.txt 
    def get_all_usernames(self) -> list:
        with open(self.username_file_path, 'r') as f:
            self.usernames = f.read().splitlines()
        return self.usernames

    def add_username(self, username) -> bool:
        with open(self.username_file_path, 'a') as f:
            f.write(username + '\n')
            return True

    # Removes the specified username from the username list
    def remove_username(self, username) -> bool:
        with open(self.username_file_path, 'r') as f:
            lines = f.readlines()
        with open(self.username_file_path, 'w') as f:
            removed_text = any(username in line and line.replace(username, '') for line in lines)
            f.writelines(line for line in lines if username not in line)
            return removed_text

    # Please refer to README.md for more information on accessible fields/ metadata
    def extract_tweet_metadata(self, tweet) -> dict:
        metadata = {\
        'username': tweet.user.username, \
        'url': tweet.url, \
        'datetime': tweet.date.strftime('%m/%d/%y %H:%M:%S'), \
        'renderdContent': tweet.renderedContent \
        }

        return metadata

    def update_stored_data(self) -> None:
        pass

    def get_latest_user_metadata(self, username) -> None:
        scraper = sntwitter.TwitterSearchScraper(username)

        # Retrieves top self.NUMBER_OF_SCRAPED_TWEETS tweets from each username
        count = 0
        df = None
        for tweet in scraper.get_items():
            count += 1
            metadata = self.extract_tweet_metadata(tweet)

            # Append metadata to dataframe
            if df is None:
                df = pd.DataFrame(metadata, index=[0])
            else:
                df.loc[len(df)] = metadata

            # Exit loop when we have enough tweets    
            if count >= self.NUMBER_OF_SCRAPED_TWEETS: break
        print(df)

    
    def run(self) -> None:
        usernames = self.get_all_usernames()
        for username in usernames:
            df = self.get_latest_user_metadata(username)
    
if __name__ == "__main__":
    twitter_api = TwitterAPI()
    # print(twitter_api.get_latest_user_tweets('fredsala'))
    twitter_api.run()
    # twitter_api.remove_username('teijin9000')
    # print(twitter_api.get_usernames())
