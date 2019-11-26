from flask import Flask, \
    jsonify, \
    url_for, \
    request, \
    render_template

app = Flask(__name__)


@app.route('/')
def test():
    return "Hello World!"

@app.route('/hello')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template("hello.html", name=(name or "young man"))


@app.route('/news/classify', methods=["POST", "GET"])
def news_classify():
    if request.method == "POST":
        return "This is a News Classify"
    if request.method == "GET":
        return "This is a News Classify"


if __name__ == '__main__':
    # app.run()

    with app.test_request_context('/hello', method='GET'):  # 单元测试
        print(request.path, request.method)
        print(url_for("test", next="cza"))
        print(url_for("news_classify"))
        print(url_for("static", filename="style.css"))
