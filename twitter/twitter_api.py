import os
import requests
import re
from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver
from selenium.webdriver.common import desired_capabilities
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

import subprocess
import configparser

import usr_mgmt

class TwitterAPI:

    def __init__(self):
        # Load environment variables from .env file
        # env_path = pathlib2.Path('..') / '.env'
        # load_dotenv(dotenv_path=env_path)

        self.usernames = []
        self.driver = self.web_driver_init() 

    def web_driver_init(self):
        # Create Firefox options object
        # firefox_options = Options()
        firefox_options = webdriver.FirefoxOptions()
        # Run firefox in headless mode
        # firefox_options.add_argument("--headless")
        # Instantiate the Firefox webdriver

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
            sleep(3)

            username = self.driver.find_element(By.XPATH, "//input[@name='text']")
            username.click()
            username.send_keys(config.get('Credentials', 'email'))
            sleep(1)

            print('email input done')

            # Find the 'Next' button (second last button (idx: -2)) using its XPATH and click it to move to the password field
            next_button = self.driver.find_elements(By.XPATH,"//div[@role='button']")[-2]
            next_button.click()

            print('Next button done')

            # Wait for the next page to load before continuing
            sleep(5)

            unusual_activity_detection = self.driver.find_element(By.XPATH, "//span[contains(text(), 'There was unusual login')]")
            unusual_username = self.driver.find_element(By.XPATH, "//input[@name='text']")
            unusual_username.click()

            unusual_username.send_keys(config.get('Credentials', 'username'))
            sleep(1)

            next_button = self.driver.find_element(By.XPATH, "//span[contains(text(), 'Next')]")
            next_button.click()

            # Reenter your password again
            reenter_password = self.driver.find_element(By.XPATH, "//input[@type='password']")
            reenter_password.click()
            reenter_password.send_keys(config.get('Credentials', 'password'))
            sleep(1)


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
            sleep(1)

            # Click Log in
            # Find the 'Log in' button using its XPATH and click it to log in
            log_in = self.driver.find_element(By.XPATH,"//span[contains(text(),'Log in')]")
            log_in.click()

            print('Login button done')

        
        # Search account
        try:

            sleep(5)
            keyword = "fredsala"
            self.driver.get(f'https://twitter.com/{keyword}')
            sleep(3)

            print(self.driver.current_url)

            # Get first tweet 
            # tweet = self.driver.find_elements(By.XPATH, '//div[@aria-label="Share Tweet"]')[0]
            # tweet.click()
            # sleep(0.5)
            # click_to_copy = self.driver.find_element(By.XPATH, '//span[contains(text(), "Copy link to Tweet")]')
            # click_to_copy.click()
            
            # tweet = self.driver.find_elements(By.XPATH, '//div[@data-testid="tweetText"]')[0]
            # tweet.click()


            url = self.driver.current_url
            r = requests.get(url)
            sleep(6)
          
            save = ActionChains(self.driver).key_down(Keys.CONTROL).key_down('s').key_up(Keys.CONTROL).key_up('s')
            save.perform()

            soup = BeautifulSoup(r.content, 'html5lib')

            file_path = "html_dump.html"
            with open(file_path, "w") as file:
                file.write(soup.prettify())




        except Exception as e:
            print(f"An exception was thrown: {type(e)}")
            print(e)
        finally:
            # self.driver.close()
            # self.driver.quit()
            pass



    def get_user_metadata(self, username) -> None:
        pass

    
    def run(self) -> None:
        self.usernames = usr_mgmt.get_all_usernames()
        self.twitter_login()
        print(self.usernames)
    
if __name__ == "__main__":
    twitter_api = TwitterAPI()
    twitter_api.run()
