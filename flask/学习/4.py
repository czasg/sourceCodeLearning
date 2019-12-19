from flask import Flask, Blueprint

app = Flask(__name__)
users = Blueprint("users", __name__)

@app.route("/")
def tt(): return "this is index"

@users.route("/user")
def test():
    return "hello world"

if __name__ == '__main__':
    app.register_blueprint(users, url_prefix="/test")
    app.run(port=8888)
