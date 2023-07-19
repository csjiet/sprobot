import os
import requests
import json
import pandas as pd
from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
from pathlib import Path

import usr_mgmt

class TwitterAPI:

    def __init__(self):
        # Load environment variables from .env file
        env_path = Path('..') / '.env'
        load_dotenv(dotenv_path=env_path)

        self.usernames = []
        self.driver = self.web_driver_init() 

    def web_driver_init(self):
        # Create Firefox options object
        firefox_options = Options()
        # Run firefox in headless mode
        firefox_options.add_argument("--headless")
        # Instantiate the Firefox webdriver
        return webdriver.Firefox(options=firefox_options) 


    def twitter_login(self):
        try:
            self.driver.get("https://twitter.com/login")
            sleep(3)

            username = self.driver.find_element(By.TAG_NAME, "input")
            username.send_keys(os.environ['TWITTER_USERNAME'])

            # Find the 'Next' button (second last button (idx: -2)) using its XPATH and click it to move to the password field
            next_button = self.driver.find_elements(By.XPATH,"//div[@role='button']")[-2]
            next_button.click()

            # Wait for the next page to load before continuing
            sleep(5)
            # Find the password input field 
            password= self.driver.find_element(By.XPATH,'//input[@type="password"]')


            password.send_keys(os.environ['TWITTER_PASSWORD'])

            # Find the 'Log in' button using its XPATH and click it to log in
            log_in = self.driver.find_element(By.XPATH,"//span[contains(text(),'Log in')]")
            log_in.click()

            sleep(5)
            keyword = "fredsala"
            self.driver.get(f"https://twitter.com/{keyword}") 
            tweets = self.driver.find_elements(By.XPATH, "//svg[@aria-hidden='true']")
            print(tweets)
            sleep(1)
        except selenium.common.exceptions as e:
            print("Already logged in")
            self.driver.exit()




    def get_user_metadata(self, username) -> None:
        pass

    
    def run(self) -> None:
        self.usernames = usr_mgmt.get_all_usernames()
        self.twitter_login()
        print(self.usernames)
    
if __name__ == "__main__":
    twitter_api = TwitterAPI()
    twitter_api.run()
