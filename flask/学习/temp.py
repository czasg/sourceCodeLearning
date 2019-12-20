from flask import Flask, Blueprint, request, abort

app = Flask(__name__)
bp = Blueprint("bp", __name__)


@app.route("/")
def index():
    return "hei"


@bp.route("/")
def test():
    return "test"


@app.route("/mul/ha/hi")
def mul():
    # return "cza", 200, ("Content-Type","text/html")
    return "cza", 200


@bp.before_request  # app.before_request_funcs[self.name].append
def bp_req():
    pass


@app.before_request
def ha():
    if request.method == "GET" and request.args.get("pass") == "cza":
        pass
    else:
        abort(404)


@app.url_value_preprocessor
def funcfunc(endpoint, view_args):
    # print(endpoint, view_args)
    ...


if __name__ == '__main__':
    app.register_blueprint(bp, url_prefix="/bp")  # will register func into flask-app
    app.run(port=8888)

    # from werkzeug.routing import Map, Rule
    #
    # map = Map([
    #     Rule('/', endpoint='index'),
    #     Rule('/downloads', endpoint='downloads/index'),
    #     Rule('/downloads/<int:id>', endpoint='downloads/show')
    # ])
    # urls = map.bind("example.com", "/")
    # print(urls.match("/", "GET"))
    # print(urls.match("/downloads"))
    # print(urls.match("/downloads/42"))
