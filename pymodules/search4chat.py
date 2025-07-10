from .common import do_auth, is_user, get_username, get_chat_name, get_chat_id


def find_chats(search_line):
    results = []

    # check if search_line is username
    user_id = find_user_id(search_line)
    if user_id == None:
        pass
    else:
        username = search_line
        new_line = {"type": "user", "user_id": user_id, "username": username}
        results.append(new_line)

    # check if search_line is user_id
    if is_user(search_line):
        user_id = search_line
        username = get_username(user_id)
        new_line = {"type": "user", "user_id": user_id, "username": username}
        results.append(new_line)
    else:
        pass

    # check if search_line is chat_name
    chat_id = get_chat_id(search_line)
    if chat_id == None:
        pass
    else:
        chat_name = search_line
        new_line = {"type": "chat", "chat_id": chat_id, "chat_name": chat_name}
        results.append(new_line)

    # check if search_line is chat_id
    if is_chat(search_line):
        chat_id = search_line
        chat_name = get_chat_name(chat_id)
        new_line = {"type": "chat", "chat_id": chat_id, "chat_name": chat_name}
        results.append(new_line)
    else:
        pass

    return results


# main func
def search_for_chat(content):
    user_id = content['user_id']
    key = content['key']
    authKey = "dummy" # content['authKey']

    if do_auth(user_id, key, authKey) != "ok":
        return "<p>access denied</p>"

    search_line = content['search_line']
    chats = find_chats(search_line)
    return chats
