import os
import slack
from twitter_api import TwitterAPI
from pathlib import Path
from dotenv import load_dotenv


class SlackBot:
    def __init__(self):
        env_path = Path('.') / '.env'
        load_dotenv(dotenv_path=env_path)

        # Slack tokens
        self._SLACK_API_TOKEN = os.environ['SLACK_API_TOKEN']
        # Twitter tokens
        self._TWITTER_API_KEY = os.environ['TWITTER_API_KEY']
        self._TWITTER_API_KEY_SECRET = os.environ['TWITTER_API_KEY_SECRET']
        self._TWITTER_ACCESS_TOKEN = os.environ['TWITTER_ACCESS_TOKEN']
        self._TWITTER_ACCESS_TOKEN_SECRET = os.environ['TWITTER_ACCESS_TOKEN_SECRET']

        self.twitter_api = TwitterAPI()


    def run(self):
        # Create a Slack client
        slack_client = slack.WebClient(token=self._SLACK_API_TOKEN)
        slack_client.chat_postMessage(channel='#research', text="Hello World!")



