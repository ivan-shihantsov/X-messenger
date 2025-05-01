from flask import Flask, app, request, jsonify
import json

app = Flask(__name__)

users_file = "data/users.json"
chats_file = "data/chats.json"
msgs_file = "data/messages.json"
UIC_file = "data/users_in_chats.json"


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


def is_user(user_id):
    with open(users_file, 'r') as jsonfile:
        data = json.load(jsonfile)
    
    for i in range(0, len(data)):
        if user_id == data[i]['user_id']:
            return True
        else:
            continue
    return False


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

    # generate
    datetime_now = "2025-04-06"
    user_id = create_user_record(username, key, datetime_now)
    return user_id


def is_chat(chat_id):
    with open(chats_file, 'r') as jsonfile:
        data = json.load(jsonfile)

    for i in range(0, len(data)):
        if str(chat_id) == data[i]['chat_id']:
            return True
        else:
            continue
    return False


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
        if chats_ids[i] == data[i]['chat_id']:
            chats_info.append(data[i])

    return chats_info


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


def save_message(chat_id, msg, user_id):
    if is_user(user_id) == False:
        return None

    with open(msgs_file, 'r') as jsonfile:
        data = json.load(jsonfile)
    msg_id = len(data) + 1

    # generate later
    created_at = "2025-04-20"

    new_msg = {"msg_id": str(msg_id), "chat_id": chat_id, "text": msg, "created_at": created_at, "from_user": user_id}
    data.append(new_msg)

    with open(msgs_file, 'w') as jsonfile:
        json.dump(data, jsonfile)
    
    return "ok"


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

    # generate later
    created_at = "2025-04-20"

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


@app.route("/signin", methods = ['POST'])
def signIn():
    content = request.json

    user_id = content['user_id']
    key = content['key']
    authKey = "dummy" # content['authKey']
    
    if do_auth(user_id, key, authKey) == "ok":
        return "<p>access allowed</p>"
    else:
        return "<p>access denied</p>"


@app.route("/signup", methods = ['POST'])
def signUp():
    content = request.json

    username = content['username']
    key = content['key']
    
    user_id = create_user(username, key)
    if user_id == None:
        return "<p>cannot create user</p>"
    else:
        return jsonify(user_id)


@app.route("/sendmsg", methods = ['POST'])
def sendMsg():
    content = request.json

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

    return jsonify({"answer":"good"})


@app.route("/getmsgs", methods = ['POST'])
def getMsgs():
    content = request.json

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
        return jsonify(messages)


@app.route("/getchats", methods = ['POST'])
def getChats():
    content = request.json

    user_id = content['user_id']
    key = content['key']
    authKey = "dummy" # content['authKey']

    if do_auth(user_id, key, authKey) != "ok":
        return "<p>access denied</p>"

    chats_list = get_user_chats(user_id)
    if chats_list == None:
        return "<p>access denied</p>"
    else:
        return jsonify(chats_list)


@app.route("/add2chat", methods = ['POST'])
def addToChat():
    content = request.json

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
    return jsonify({"chat_id":str(chat_id)})


# localhost:8001 - keep for testing
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


# http://127.0.0.1:8001/home - keep for testing
@app.route("/home")
def home():
    return "<p>home page!!!</p>"


if __name__ == "__main__":
    app.run(debug=True, port=8001)
