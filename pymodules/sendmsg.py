import json
from .common import do_auth, is_user, is_user_in_chat, get_datetime_now


msgs_file = "data/messages.json"


def save_message(chat_id, msg, user_id):
    if is_user(user_id) == False:
        return None

    with open(msgs_file, 'r') as jsonfile:
        data = json.load(jsonfile)
    msg_id = len(data) + 1

    created_at = get_datetime_now()

    new_msg = {"msg_id": str(msg_id), "chat_id": chat_id, "text": msg, "created_at": created_at, "from_user": user_id}
    data.append(new_msg)

    with open(msgs_file, 'w') as jsonfile:
        json.dump(data, jsonfile)
    
    return "ok"


# main func
def send_msg(content):
    user_id = content['user_id']
    key = content['key']
    authKey = "dummy" # content['authKey']

    if do_auth(user_id, key, authKey) != "ok":
        return "<p>access denied</p>"

    to_chat = content['chat_id']

    if is_user_in_chat(user_id, to_chat) == False:
        return "<p>access denied</p>"

    msg = content['msg']
    if save_message(to_chat, msg, user_id) == None:
        return "<p>access denied</p>"

    return {"answer":"good"}
