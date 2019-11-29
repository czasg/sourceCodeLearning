from flask import Flask, session, jsonify, request, make_response

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cza'

@app.route('/')
def index():
    session['username'] = 'cza'
    print(request.cookies.get('session', 'None Cookies'), request.cookies.get('ha', 'None Find'))
    response = make_response(jsonify(dict(session.items())))
    response.set_cookie('ha', 'lo')
    return response

@app.route('/test2')
@app.route('/test2/<value>')
def test2(value=None):
    session['username2'] = value or 'cza2'
    print(request.cookies.get('session', 'None Cookies'), request.cookies.get('ali', 'None Find'))
    response = make_response(jsonify(dict(session.items())))
    response.set_cookie('ali', 'loh')
    return response

@app.route('/get/<username>')
def get_username(username):
    return session.get(username)


if __name__ == '__main__':
    app.run()

