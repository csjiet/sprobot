import sys
sys.path.insert(1, './twitter')
import ssl
import configparser
import slack
from twitter_api import TwitterAPI


class SlackBot:
    def __init__(self):

        # Slack tokens
        config = configparser.ConfigParser()
        config.read(f'{sys.path[1]}/config.ini')
        self._SLACK_API_TOKEN = config.get('Credentials','slack_api_token')
        self.twitter_api = TwitterAPI()
        self.latest_usr_tweet_pair = self.twitter_api.get_user_latest_tweets()

        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE
        # Create a Slack client
        self.slack_client = slack.WebClient(token=self._SLACK_API_TOKEN, ssl=self.ssl_context)

        self.slack_channels = ['#research']

    def notification_text_wrapper(self, real_content, *argv):
        text = f"New tweet alert!\n{real_content}\nI am up for 10 days!" 
        return text

    def notification_alarm(self , content):
        for channel in self.slack_channels:
            if content is not None:
                self.slack_client.chat_postMessage(channel= channel, text=content)

    # TODO: filter_func should filter tweet that should be notified
    def status_checker(self, filter_func):
        consumer = self.latest_usr_tweet_pair
        producer = self.twitter_api.get_user_latest_tweets()

        # Check if consumer - local copy of user-tweet pair and producer - twitter api tweets are in sync
        for key in producer:
            if key not in consumer:
                self.notification_alarm(producer[key])
            if consumer[key] != producer[key]:
                self.notification_alarm(producer[key])

    def sync_tweet_consumer_producer(self):
        self.latest_usr_tweet_pair = self.twitter_api.get_user_latest_tweets()

    def run(self):
        text = self.notification_text_wrapper("https://twitter.com/stevebach/status/1678756180196204545")
        self.notification_alarm(text)

if __name__ == "__main__":
    bot = SlackBot()
    bot.run()
