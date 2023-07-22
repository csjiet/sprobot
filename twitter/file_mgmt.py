import json

# This file contains user management functions

class FileMgmt:

    def __init__(self):
        # self.username_file_path = './twitter/usernames.txt'
        # self.user_tweet_json_file_path = './twitter/users_latest_tweets.json'
        
        self.username_file_path = f'./twitter/usernames.txt'
        self.user_tweet_json_file_path = f'./twitter/users_latest_tweets.json'

    # Reads the latest list of usernames from username_list.txt 
    def read_all_usernames_from_file(self) -> list:
        usernames = []
        with open(self.username_file_path, 'r') as f:
            usernames = f.read().splitlines()
        return usernames

    def write_username_list_to_file(self, username_list) -> bool:
        with open(self.username_file_path, "w") as f:
            for usr in username_list:
                f.write(str(usr) + "\n")
            return True

    def write_username_tweet_dict_to_file(self, user_latest_tweets) -> bool:
        with open(self.user_tweet_json_file_path, "w") as f:
            json.dump(user_latest_tweets, f, indent = 4)
            return True
