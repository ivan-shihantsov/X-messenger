from flask import Flask, app, request, jsonify
import json

app = Flask(__name__)

users_file = "data/users.txt"
chats_file = "data/chats.txt"
msgs_file = "data/messages.txt"
UIC_file = "data/users_in_chats.txt"


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


def is_user_in_chat(user_id, chat_id):
    if is_user(user_id) == False:
        return False

    with open(UIC_file, 'r') as jsonfile:
        data = json.load(jsonfile)

    for i in range(0, len(data)):
        if user_id == data[i]['user_id'] and chat_id == data[i]['chat_id']:
            return True
    return False


def get_new_msgs(chat_id, last_msg_id):
    pass


def save_message(chat_id, msg, user_id):
    if is_user(user_id) == False:
        return None

    with open(msgs_file, 'r') as jsonfile:
        data = json.load(jsonfile)
    msg_id = len(data) + 1

    # generate later
    created_at = "2025-04-20"

    new_msg = {"msg_id": msg_id, "chat_id": chat_id, "text": msg, "created_at": created_at, "from_user": user_id}
    data.append(new_msg)

    with open(msgs_file, 'w') as jsonfile:
        json.dump(data, jsonfile)
    
    return "ok"



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
