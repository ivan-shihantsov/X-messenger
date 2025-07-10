import json
from .common import do_auth, is_user, is_chat, is_user_in_chat, get_datetime_now


chats_file = "data/chats.json"
UIC_file = "data/users_in_chats.json"


def add_to_chat(user_id, to_chat_id):
    if is_chat(to_chat_id) == False:
        return None

    if is_user_in_chat(user_id, to_chat_id):
        return to_chat_id

    with open(UIC_file, 'r') as jsonfile:
        data = json.load(jsonfile)

    link_id = len(data) + 1
    new_link = {"link_id": str(link_id), "user_id": user_id, "chat_id": str(to_chat_id)}
    data.append(new_link)

    with open(UIC_file, 'w') as jsonfile:
        json.dump(data, jsonfile)

    return to_chat_id


def create_new_chat(admin, chat_name):
    with open(chats_file, 'r') as jsonfile:
        data = json.load(jsonfile)

    chat_id = len(data) + 1

    created_at = get_datetime_now()

    # default color
    color = "#f06359"

    new_chat = {"chat_id": str(chat_id), "chat_name": chat_name, "color": color, "created_at": created_at, "admin": admin}
    data.append(new_chat)

    with open(chats_file, 'w') as jsonfile:
        json.dump(data, jsonfile)

    return chat_id


def create_chat(user_id, to_user_id, chat_name):
    if is_user(user_id) == False and is_user(to_user_id) == False:
        return None

    chat_id = create_new_chat(user_id, chat_name)
    add_to_chat(user_id, chat_id)
    add_to_chat(to_user_id, chat_id)

    return chat_id


# main func
def add_to_chat(content):
    user_id = content['user_id']
    key = content['key']
    authKey = "dummy" # content['authKey']

    if do_auth(user_id, key, authKey) != "ok":
        return "<p>access denied</p>"

    to_chat_id = None
    to_user_id = None

    try:
        to_chat_id = content['to_chat_id']
    except KeyError:
        pass

    try:
        to_user_id = content['to_user_id']
    except KeyError:
        if to_chat_id == None:
            return "<p>access denied</p>"

    if to_chat_id != None and to_user_id == None:
        chat_id = add_to_chat(user_id, to_chat_id)
        if chat_id == None:
            return "<p>access denied</p>"
    elif to_chat_id == None and to_user_id != None:
        chat_name = content['chat_name']
        chat_id = create_chat(user_id, to_user_id, chat_name)
        if chat_id == None:
            return "<p>access denied</p>"
    else:
        return "<p>access denied</p>"
    return {"chat_id":str(chat_id)}
