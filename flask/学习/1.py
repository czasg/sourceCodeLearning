from flask import Flask, jsonify, url_for, request

app = Flask(__name__)


@app.route('/')
def test():
    return "Hello World!"


@app.route('/news/classify', methods=["POST", "GET"])
def news_classify():
    if request.method == "POST":
        return "This is a News Classify"
    if request.method == "GET":
        pass


if __name__ == '__main__':
    # app.run()

    with app.test_request_context():
        print(url_for("test", next="cza"))
        print(url_for("news_classify"))
