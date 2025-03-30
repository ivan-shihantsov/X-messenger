from flask import Flask, app, request, jsonify

app = Flask(__name__)


# http://127.0.0.1:8001/
# localhost:8001
# just for testing
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


# http://127.0.0.1:8001/home
# localhost:8001/home
# also just for fun
@app.route("/home")
def home():
    return "<p>home page!!!</p>"


@app.route("/sendMsg", methods = ['GET', 'POST'])
def sendMsg():
    if request.method == 'POST':
        content = request.json

        username = content['username']
        toUser = content['toUser']
        msg = content['msg']

        print(f"user '{username}' writes to '{toUser}' a message: '{msg}'")
        return jsonify({"answer":"good"})
    else:
        return "<p>this must be POST request</p>"


if __name__ == "__main__":
    app.run(debug=True, port=8001)
