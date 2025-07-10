import json
from .common import do_auth, is_user_in_chat, is_msg_in_chat


msgs_file = "data/messages.json"


def get_new_msgs(chat_id, last_msg_id):
    if is_msg_in_chat(last_msg_id, chat_id) == False:
        return None

    with open(msgs_file, 'r') as jsonfile:
        data = json.load(jsonfile)

    msgs_list = []

    # no messages on client - get all
    if int(last_msg_id) == -1:
        for i in range(0, len(data)):
            if data[i]['chat_id'] == chat_id:
                msgs_list.append(data[i])
    # get since the last message
    else:
        for i in range(int(last_msg_id), len(data)):
            if data[i]['chat_id'] == chat_id:
                msgs_list.append(data[i])

    return json.dumps(msgs_list)


# main func
def get_msgs(content):
    user_id = content['user_id']
    key = content['key']
    authKey = "dummy" # content['authKey']

    if do_auth(user_id, key, authKey) != "ok":
        return "<p>access denied</p>"

    in_chat = content['chat_id']

    if is_user_in_chat(user_id, in_chat) == False:
        return "<p>access denied</p>"
    
    last_msg_id = content['last_msg_id']
    messages = get_new_msgs(in_chat, last_msg_id)
    if messages == None:
        return "<p>access denied</p>"
    else:
        return messages
