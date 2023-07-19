# This file contains user management functions
username_file_path = './usernames.txt'

# Reads the latest list of usernames from username_list.txt 
def get_all_usernames() -> list:
    with open(username_file_path, 'r') as f:
        usernames = f.read().splitlines()
    return usernames

def add_username(username) -> bool:
    with open(username_file_path, 'a') as f:
        f.write(username + '\n')
        return True

# Removes the specified username from the username list
def remove_username(username) -> bool:
    with open(username_file_path, 'r') as f:
        lines = f.readlines()
    with open(username_file_path, 'w') as f:
        removed_username = any(username in line and line.replace(username, '') for line in lines)
        f.writelines(line for line in lines if username not in line)
        return removed_username 