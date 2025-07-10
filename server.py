from flask import Flask, app, request, jsonify
from pymodules import *


app = Flask(__name__)


@app.route("/signin", methods = ['POST'])
def signIn():
    content = request.json
    return signin.sign_in(content)


@app.route("/signup", methods = ['POST'])
def signUp():
    content = request.json
    return jsonify(signup.sign_up(content))


@app.route("/sendmsg", methods = ['POST'])
def sendMsg():
    content = request.json
    return jsonify(sendmsg.send_msg(content))


@app.route("/getmsgs", methods = ['POST'])
def getMsgs():
    content = request.json
    return jsonify(getmsgs.get_msgs(content))


@app.route("/getchats", methods = ['POST'])
def getChats():
    content = request.json
    return jsonify(getchats.get_chats(content))


@app.route("/add2chat", methods = ['POST'])
def addToChat():
    content = request.json
    return jsonify(add2chat.add_to_chat(content))


@app.route("/search4chat", methods = ['POST'])
def search4chat():
    content = request.json
    return jsonify(search4chat.search_for_chat(content))


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
