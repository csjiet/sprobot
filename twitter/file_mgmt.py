# This file contains user management functions

class FileMgmt:

    def __init__(self):
        self.username_file_path = './usernames.txt'

    # Reads the latest list of usernames from username_list.txt 
    def read_all_usernames_from_file(self) -> list:
        with open(self.username_file_path, 'r') as f:
            usernames = f.read().splitlines()
        return usernames

    def write_username_to_file(self, username) -> bool:
        with open(self.username_file_path, 'a') as f:
            f.write(username + '\n')
            return True

    # Removes the specified username from the username list
    def delete_username_from_file(self, username) -> bool:
        with open(self.username_file_path, 'r') as f:
            lines = f.readlines()
        with open(self.username_file_path, 'w') as f:
            removed_username = any(username in line and line.replace(username, '') for line in lines)
            f.writelines(line for line in lines if username not in line)
            return removed_username 
