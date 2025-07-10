import json
from .common import do_auth, is_user


chats_file = "data/chats.json"
UIC_file = "data/users_in_chats.json"


def get_user_chats(user_id):
    if is_user(user_id) == False:
        return None

    chats_ids = []
    with open(UIC_file, 'r') as jsonfile:
        data = json.load(jsonfile)

    for i in range(0, len(data)):
        if user_id == data[i]['user_id']:
            chats_ids.append(data[i]['chat_id'])

    chats_info = []

    with open(chats_file, 'r') as jsonfile:
        data = json.load(jsonfile)

    for i in range(0, len(data)):
        for j in range(0, len(chats_ids)):
            if chats_ids[j] == data[i]['chat_id']:
                chats_info.append(data[i])

    return chats_info


# main func
def get_chats(content):
    user_id = content['user_id']
    key = content['key']
    authKey = "dummy" # content['authKey']

    if do_auth(user_id, key, authKey) != "ok":
        return "<p>access denied</p>"

    chats_list = get_user_chats(user_id)
    if chats_list == None:
        return "<p>access denied</p>"
    else:
        return chats_list
