import os
import random
import json
import configparser
import sys
from time import sleep
from selenium import webdriver
from selenium.webdriver.common import desired_capabilities
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from file_mgmt import FileMgmt 

class TwitterAPI:

    def __init__(self):

        self.file_management = FileMgmt() 
        self.driver = None 
        self.usernames = self.file_management.read_all_usernames_from_file()

        self.usr_latest_tweets = {}
        
        with open(f"./twitter/users_latest_tweets.json") as jsonfile:
            self.usr_latest_tweets = json.load(jsonfile) 

        # Sync the user-tweet pairs to list of usernames from username.txt
        self.usr_latest_tweets = {key: self.usr_latest_tweets[key] for key in self.usernames if key in self.usr_latest_tweets}

    def get_usernames(self):
        return self.usernames

    def get_user_latest_tweets(self):
        return self.usr_latest_tweets.copy()

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
  
    def twitter_login(self) -> None:
        # Login Twitter
        try:
            config = configparser.ConfigParser()
            config.read('./twitter/config.ini')

            self.driver.get("https://twitter.com/i/flow/login")
            sleep(random.choice([6,4,5]))

            username = self.driver.find_element(By.XPATH, "//input[@name='text']")
            username.click()
            username.send_keys(config.get('Credentials', 'email'))
            sleep(random.choice([1,3,1.2]))

            # Find the 'Next' button (second last button (idx: -2)) using its XPATH and click it to move to the password field
            next_button = self.driver.find_elements(By.XPATH,"//div[@role='button']")[-2]
            next_button.click()

            # Wait for the next page to load before continuing
            sleep(random.choice([5.234,6.3]))

            unusual_activity_detection = self.driver.find_element(By.XPATH, "//span[contains(text(), 'There was unusual login')]")
            unusual_username = self.driver.find_element(By.XPATH, "//input[@name='text']")
            unusual_username.click()

            unusual_username.send_keys(config.get('Credentials', 'username'))
            sleep(random.choice([1,1.3]))

            next_button = self.driver.find_element(By.XPATH, "//span[contains(text(), 'Next')]")
            next_button.click()

            # Reenter your password again
            reenter_password = self.driver.find_element(By.XPATH, "//input[@type='password']")
            sleep(1)
            reenter_password.click()
            reenter_password.send_keys(config.get('Credentials', 'password'))
            sleep(random.choice([1.36,1.43]))


            # Click Log in
            # Find the 'Log in' button using its XPATH and click it to log in
            log_in = self.driver.find_element(By.XPATH,"//span[contains(text(),'Log in')]")
            log_in.click()



        except Exception as e:
            # Proceed to normal login
            print(f'Dang exception again: {str(type(e))} {str(e)}')
           
            sleep(3)
            # Reenter your password again
            reenter_password = self.driver.find_element(By.XPATH, "//input[@type='password']")
            sleep(1)
            reenter_password.click()
            reenter_password.send_keys(config.get('Credentials', 'password'))
            sleep(random.choice([1.1,2.1]))

            # Click Log in
            # Find the 'Log in' button using its XPATH and click it to log in
            log_in = self.driver.find_element(By.XPATH,"//span[contains(text(),'Log in')]")
            log_in.click()

       
    def update_latest_tweets(self, username, tweet_link) -> None:

        # Only update if it is a non-null value
        if self.usr_latest_tweets[username] is not None and tweet_link is None:
            return


        self.usr_latest_tweets[username] = tweet_link

    def username_search(self, username) -> None:
        # Search account
        try:
            sleep(5)
            # Visit personnel's website
            self.driver.get(f'https://twitter.com/{username}')
            sleep(random.choice([6,5.1,5,7.2]))
            sleep(6) # TODO: Should be removed - added to compensate for slow internet connection

            self.driver.execute_script("window.scrollTo(0, 500)")

            action = ActionChains(self.driver)

            source = self.driver.find_elements(By.XPATH, "//div[@data-testid='tweetText']")[0]
            action.move_to_element(source).click().perform()
            return self.driver.current_url


        except Exception as e:
            print(f"Non fatal exception was caught: {type(e)} + {e}")

    # Add username to username buffer 
    def add_username(self, username_to_add) -> None:

        # Check if username has already been added
        if username_to_add in self.usernames:
            return

        # Append object to username buffer
        self.usernames.append(username_to_add)

        # Add object as key to the username-tweet dictionary
        self.usr_latest_tweets.setdefault(username_to_add, None)


    # Remove username from username buffer 
    def remove_username(self, username_to_remove) -> None:

        # Check if username has already been removed
        if username_to_remove not in self.usernames:
            return

        # Remove object from usernames list
        self.usernames = [usr for usr in self.usernames if usr != username_to_remove]

        # Remove key value pair where key matches removed username
        self.usr_latest_tweets = {key: value for key, value in self.usr_latest_tweets.items() if key in self.usernames}


    # Write all buffers to files
    def sync_buffer_with_files(self) -> None:
        self.file_management.write_username_list_to_file(self.usernames)
        self.file_management.write_username_tweet_dict_to_file(self.usr_latest_tweets)
        return None


    # Webscraping cycle
    def run(self) -> None:
        self.driver = self.web_driver_init()
        try:
            self.twitter_login()
        except:
            self.driver.close()
            self.driver.quit()
            self.driver = None
            os.system("pkill firefox")
            print("Timeout. Retry login in ~20min")
            sleep(random.choice([60*20.2, 60*19.3]))
            self.driver = self.web_driver_init()
            self.twitter_login()
        for username in self.usernames:
            print(f"Searching @{username} ...")
            tweet_link = self.username_search(username)
            self.update_latest_tweets(username, tweet_link)
        
        # print(str(self.usr_latest_tweets))
        sleep(random.choice([1,2,4.3,4.75,5,3.14]))
        self.driver.close()
        self.driver.quit()
        self.driver = None

    
if __name__ == "__main__":
    sys.path.insert(1,".")
    twitter_api = TwitterAPI()
    twitter_api.run()
