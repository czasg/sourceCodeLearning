from flask import Flask, render_template, views, jsonify

app = Flask(__name__)


class JsonView(views.View):
    def get_response(self):
        raise NotImplementedError()

    def dispatch_request(self):
        response = self.get_response()
        return jsonify(response)


class IndexView(JsonView):
    def get_response(self):
        context = {
            'username': 'ivy'
        }
        return context


app.add_url_rule('/', view_func=IndexView.as_view('index'))


class FakeView(object):
    def __init__(self):
        super().__init__()
        self.context = {
            'username': 'ivy',
        }


class TestView(JsonView, FakeView):
    def get_response(self):
        self.context.update({'age': 23})
        return self.context


app.add_url_rule('/test', view_func=TestView.as_view('test'))

if __name__ == '__main__':
    app.run()
