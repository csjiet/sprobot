import sys
import ssl
sys.path.insert(0,'.')
sys.path.insert(1,'./twitter')
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


    def run(self):
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        # Create a Slack client
        slack_client = slack.WebClient(token=self._SLACK_API_TOKEN, ssl=ssl_context)
        slack_client.chat_postMessage(channel='#research', text="Hello World!")


if __name__ == "__main__":
    bot = SlackBot()
    bot.run()
