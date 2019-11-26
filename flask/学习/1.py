from flask import Flask, \
    jsonify, \
    url_for, \
    request, \
    render_template, \
    abort, redirect, session, escape

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


@app.route('/')
def test():
    return "Hello World!"


@app.route('/hello')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template("hello.html", name=(name or "young man"))


@app.route('/old')
def old_to_new():
    return redirect(url_for('hello'))


@app.route('/abort')
def abort_func():
    abort(401)
    abort(404)


@app.route('/news/classify', methods=["POST", "GET"])
def news_classify():
    if request.method == "POST":
        return "This is a News Classify"
    if request.method == "GET":
        return "This is a News Classify"


@app.route('/login')
def login():
    username = request.args.get('username', "")
    if username:
        session['username'] = username  # app.secret_key
        return redirect(url_for('after_login'))
    else:
        abort(404)


@app.route('/after/login')
def after_login():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in ! Forbidden You Pass !'


@app.route('/login/out')
def login_out():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.errorhandler(404)
def page_not_found(error):  # 调用abort(404)，则会返回此页面。这也太方便了把
    return render_template('error.html'), 404


if __name__ == '__main__':
    app.run()

    with app.test_request_context('/hello', method='GET'):  # 单元测试
        print(request.path, request.method)
        print(url_for("test", next="cza"))
        print(url_for("news_classify"))
        print(url_for("static", filename="style.css"))

"""
request.form.get('username', '')  => POST form_data
request.args.get('key', '')  =>  ?key=value
request.cookies.get('username')  => cookies

resp = make_response(render_template(...))  => set cookies
resp.set_cookie('username', 'the username')
"""
