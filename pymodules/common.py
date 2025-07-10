import json
from datetime import datetime, timezone

users_file = "data/users.json"
chats_file = "data/chats.json"
UIC_file = "data/users_in_chats.json"


def get_datetime_now():
    datetime_obj = datetime.now(timezone.utc) # UTC+0

    # 2025-07-10 13:56:38 +0000
    time_template = "%Y-%m-%d %H:%M:%S %z"
    result = datetime_obj.strftime(time_template)

    return result


def is_user(user_id):
    with open(users_file, 'r') as jsonfile:
        data = json.load(jsonfile)
    
    for i in range(0, len(data)):
        if user_id == data[i]['user_id']:
            return True
        else:
            continue
    return False


def is_chat(chat_id):
    with open(chats_file, 'r') as jsonfile:
        data = json.load(jsonfile)

    for i in range(0, len(data)):
        if str(chat_id) == data[i]['chat_id']:
            return True
        else:
            continue
    return False


def get_username(user_id):
    with open(users_file, 'r') as jsonfile:
        data = json.load(jsonfile)

    for i in range(0, len(data)):
        if user_id == data[i]['user_id']:
            username = data[i]['username']
            return username
        else:
            continue
    return None


def get_chat_name(chat_id):
    with open(chats_file, 'r') as jsonfile:
        data = json.load(jsonfile)

    for i in range(0, len(data)):
        if chat_id == data[i]['chat_id']:
            chat_name = data[i]['chat_name']
            return chat_name
        else:
            continue
    return None


def get_chat_id(chat_name):
    with open(chats_file, 'r') as jsonfile:
        data = json.load(jsonfile)

    for i in range(0, len(data)):
        if chat_name == data[i]['chat_name']:
            chat_id = data[i]['chat_id']
            return chat_id
        else:
            continue
    return None


def find_user_id(username):
    with open(users_file, 'r') as jsonfile:
        data = json.load(jsonfile)
    
    for i in range(0, len(data)):
        if username == data[i]['username']:
            user_id = data[i]['user_id']
            return user_id
        else:
            continue
    return None


def do_auth(user_id, key, authKey):
    if is_user(user_id) == False:
        return None
    
    with open(users_file, 'r') as jsonfile:
        data = json.load(jsonfile)
    
    for i in range(0, len(data)):
        if user_id == data[i]['user_id']:
            passHash = data[i]['passHash']

    if passHash == key:
        return "ok"
    else:
        return None


def is_user_in_chat(user_id, chat_id):
    if is_user(user_id) == False:
        return False

    with open(UIC_file, 'r') as jsonfile:
        data = json.load(jsonfile)

    for i in range(0, len(data)):
        if user_id == data[i]['user_id'] and chat_id == data[i]['chat_id']:
            return True
    return False


def is_msg_in_chat(msg_id, chat_id):
    with open(msgs_file, 'r') as jsonfile:
        data = json.load(jsonfile)

    for i in range(0, len(data)):
        if msg_id == data[i]['msg_id'] and chat_id == data[i]['chat_id']:
            return True
    return False
