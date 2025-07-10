import json
from .common import find_user_id, get_datetime_now


users_file = "data/users.json"


def create_user_record(username, passHash, datetime_now):
    with open(users_file, 'r') as jsonfile:
        data = json.load(jsonfile)

    user_id = len(data) + 1
    new_user = {"user_id": str(user_id), "username": username, "passHash": passHash, "created_at": datetime_now}
    data.append(new_user)

    with open(users_file, 'w') as jsonfile:
        json.dump(data, jsonfile)

    return user_id


def create_user(username, key):
    user_id = find_user_id(username)
    if user_id != None:
        return None # user exists

    datetime_now = get_datetime_now()
    user_id = create_user_record(username, key, datetime_now)
    return user_id


# main func
def sign_up(content):
    username = content['username']
    key = content['key']
    
    user_id = create_user(username, key)
    if user_id == None:
        return "<p>cannot create user</p>"
    else:
        return user_id
