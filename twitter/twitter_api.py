import random
import json
from time import sleep
from selenium import webdriver
from selenium.webdriver.common import desired_capabilities
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

import configparser

from file_mgmt import FileMgmt 

class TwitterAPI:

    def __init__(self):

        self.file_management = FileMgmt() 
        self.driver = self.web_driver_init() 
      
        self.usr_latest_tweets = {}
        with open("users_latest_tweets.json") as jsonfile:
            self.usr_latest_tweets = json.load(jsonfile) 



    def web_driver_init(self):
        # Create Firefox options object
        firefox_options = webdriver.FirefoxOptions()

        # Checks if device has a monitor 
        driver = None
        try:
            driver = webdriver.Firefox(options=firefox_options) 

        # If device does nto have a monitor, run browser using the headless option
        except Exception as e:
            firefox_options.add_argument("--headless")
            firefox_options.add_argument("--enable-javascript")
            firefox_options.add_argument("start-maximized")
            firefox_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)")
            firefox_options.add_argument("--disable-blink-features=AutomationControlled")
            firefox_options.set_preference("network.proxy.type", 1)
            firefox_options.set_preference("devtools.jsonview.enabled", False)
            firefox_options.set_preference("dom.webdriver.enabled", False)
            firefox_options.set_preference('useAutomationExtension', False)

            # firefox_options.preferences.update({"javascript.enabled": True,})
            driver = webdriver.Firefox(options=firefox_options)


        return driver
  
    def twitter_login(self):
        # Login Twitter
        try:
            config = configparser.ConfigParser()
            config.read('config.ini')

            self.driver.get("https://twitter.com/i/flow/login")
            sleep(random.choice([3,4,5]))

            username = self.driver.find_element(By.XPATH, "//input[@name='text']")
            username.click()
            username.send_keys(config.get('Credentials', 'email'))
            sleep(random.choice([1,3,1.2]))

            # Find the 'Next' button (second last button (idx: -2)) using its XPATH and click it to move to the password field
            next_button = self.driver.find_elements(By.XPATH,"//div[@role='button']")[-2]
            next_button.click()

            # Wait for the next page to load before continuing
            sleep(random.choice([5,6.3]))

            unusual_activity_detection = self.driver.find_element(By.XPATH, "//span[contains(text(), 'There was unusual login')]")
            unusual_username = self.driver.find_element(By.XPATH, "//input[@name='text']")
            unusual_username.click()

            unusual_username.send_keys(config.get('Credentials', 'username'))
            sleep(random.choice([1,1.3]))

            next_button = self.driver.find_element(By.XPATH, "//span[contains(text(), 'Next')]")
            next_button.click()

            # Reenter your password again
            reenter_password = self.driver.find_element(By.XPATH, "//input[@type='password']")
            reenter_password.click()
            reenter_password.send_keys(config.get('Credentials', 'password'))
            sleep(random.choice([1,1.43]))


            # Click Log in
            # Find the 'Log in' button using its XPATH and click it to log in
            log_in = self.driver.find_element(By.XPATH,"//span[contains(text(),'Log in')]")
            log_in.click()



        except Exception as e:
            # Proceed to normal login
            print('Dang exception again')
            
            # Reenter your password again
            reenter_password = self.driver.find_element(By.XPATH, "//input[@type='password']")
            reenter_password.click()
            reenter_password.send_keys(config.get('Credentials', 'password'))
            sleep(random.choice([1,2]))

            # Click Log in
            # Find the 'Log in' button using its XPATH and click it to log in
            log_in = self.driver.find_element(By.XPATH,"//span[contains(text(),'Log in')]")
            log_in.click()

            print('Login button done')

       
    def update_latest_tweets(self, username, tweet_link):
        self.usr_latest_tweets[username] = tweet_link
        print(self.usr_latest_tweets)


    def username_search(self, username):
        # Search account
        try:
            sleep(5)
            # Visit personnel's website
            self.driver.get(f'https://twitter.com/{username}')
            sleep(random.choice([3,4.1,5]))

            self.driver.execute_script("window.scrollTo(0, 500)")

            source = self.driver.find_elements(By.XPATH, "//div[@data-testid='tweetText']")[0]
            action = ActionChains(self.driver)
            action.move_to_element(source).click().perform()
            return self.driver.current_url


        except Exception as e:
            print(f"Non fatal exception was caught: {type(e)} + {e}")
        finally:
            # self.driver.close()
            # self.driver.quit()
            pass

    def sync_username_buffers(self, usernames_list):
        self.usr_latest_tweets = {key: value for key, value in self.usr_latest_tweets.items() if key in usernames_list}

    def add_username(self):
        usernames_list = self.file_management.read_all_usernames_from_file()
        self.sync_username_buffers(usernames_list)

    def remove_username(self):
        usernames_list = self.file_management.read_all_usernames_from_file()
        self.sync_username_buffers(usernames_list)


        

    def run(self) -> None:
        self.twitter_login()
        usernames = self.file_management.read_all_usernames_from_file()
        for username in usernames:
            tweet_link = self.username_search(username)
            self.update_latest_tweets(username, tweet_link)

        with open("users_latest_tweets.json", "w") as op:
            json.dump(self.usr_latest_tweets, op, indent = 4)


    
if __name__ == "__main__":
    twitter_api = TwitterAPI()
    twitter_api.run()
