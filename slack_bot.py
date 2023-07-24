import os
import sys
import random
from datetime import datetime
from datetime import time
from time import sleep
sys.path.insert(1, "./twitter")
import ssl
import configparser
import slack
from twitter_api import TwitterAPI


class SlackBot:
    def __init__(self):

        # Instantiating Twitter api class
        self.twitter_api = TwitterAPI()
        self.latest_usr_tweet_pair = self.twitter_api.get_user_latest_tweets()

        # Retrieve Slack tokens
        config = configparser.ConfigParser()
        config.read(f'./twitter/config.ini')
        self._SLACK_API_TOKEN = config.get('Credentials','slack_api_beta_token')

        # Preparing slack ssl context
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE

        # Create a Slack client
        self.slack_client = slack.WebClient(token=self._SLACK_API_TOKEN, ssl=self.ssl_context)

        # TODO: CLI to add slack channels?
        self.slack_channels = ['#sprobot_tests']

    def notification_text_wrapper(self, real_content, **kwargv):
        final_text = f"New tweet alert from @{kwargv['username']}!\n{real_content}\n" 
        return final_text

    def notification_alarm(self , content):
        for channel in self.slack_channels:
            if content is not None:
                self.slack_client.chat_postMessage(channel= channel, text=content)

    def filter_out_non_user_content(self, **kw) -> bool:
        
        if kw['v'] is None:
            return False

        # Check if tweet is from the original owner
        if kw['k'] in kw['v']:
            return True

        return False

    # TODO: filter_func should filter tweet that should be notified
    def status_checker(self, filter_func):
        consumer = self.latest_usr_tweet_pair
        producer = self.twitter_api.get_user_latest_tweets()

        # print(f'consumer: \n {str(consumer)}')
        # print(f'producer: \n {str(producer)}')

        # Check if consumer - local copy of user-tweet pair and producer - twitter api tweets are in sync
        for key in producer:
            if key not in consumer:

                # Key is not in consumer, so add into consumer
                self.latest_usr_tweet_pair[key] = producer[key]

                if filter_func(k= key, v= producer[key]):
                    content = self.notification_text_wrapper(producer[key], username = key)
                    self.notification_alarm(content)
                    continue

            if consumer[key] != producer[key] and filter_func(k = key, v = producer[key]):
                content = self.notification_text_wrapper(producer[key], username = key)
                self.notification_alarm(content)
                continue

    def sync_tweet_consumer_producer(self):
        self.latest_usr_tweet_pair = self.twitter_api.get_user_latest_tweets()

    def is_notification_unmute(self, current_time):
        the_am_start = time(random.choice([6,7,8]), random.choice([1,2,3,4,5,6,7,8,9,10,30]))
        the_am_end= time(11,59)

        the_pm_start = time(12, 0)
        the_pm_end = time(23, random.choice([50,51,52,53,54,55,56,57,58,59]))

        # Allow between ~6/7/8am - 11.59am, 12pm - 11pm
        return the_am_start <= current_time <= the_am_end or the_pm_start <= current_time <= the_pm_end 
        # return True 

    def run(self):
        # breakpoint()
        count = 1
        while True:
            print(f"####### Run: {count}; time: {datetime.now().time()}#######")
            current_time = datetime.now().time()

            if self.is_notification_unmute(current_time):
                self.twitter_api.run()
                self.status_checker(self.filter_out_non_user_content)
                self.sync_tweet_consumer_producer()
                os.system("pkill firefox")
            self.twitter_api.sync_buffer_with_files()

            print(f"### Done! ###")
            # sleep(random.choice([3,3.2,3.7,4, 5, 5.2]))
            sleep(random.choice([60*23, 60*20, 60*26, 60*29, 60*24, 60*30]))
            count+=1
            # if count >= 20:
                # break

if __name__ == "__main__":
    bot = SlackBot()
    bot.run()
