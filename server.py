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


def create_user(username, key, authKey):
    user_id = find_user_id(username)
    if user_id != None:
        return None # user exists



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


@app.route("/sendmsg", methods = ['POST'])
def sendMsg():
    content = request.json

    user_id = content['user_id']
    key = content['key']
    authKey = "dummy" # content['authKey']

    if do_auth(user_id, key, authKey) != "ok":
        return "<p>access denied</p>"

    to_chat = content['chat_id']
    msg = content['msg']

    print(f"user with ID '{user_id}' writes to chat with ID '{to_chat}' a message: '{msg}'")
    return jsonify({"answer":"good"})



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
