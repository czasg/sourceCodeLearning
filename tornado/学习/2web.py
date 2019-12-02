import tornado.ioloop
import tornado.web
# import tornado.web.url
from tornado.web import RequestHandler



class MainHandler(RequestHandler):

    def get(self):
        self.write(f'<a href="{self.reverse_url("story", "1")}">'
                   f'link to story 1</a>')

class StoreHandler(RequestHandler):
    def initialize(self, db):
        self.db = db

    def get(self, story_id):
        self.write(f"This is story {story_id}")


def make_app():
    # AsyncIOMainLoop().install()
    return tornado.web.Application([
        url(r"/", MainHandler),
        url(r"/story/([0-9]+)", StoreHandler, dict(db=None), name="story")
    ])


if __name__ == '__main__':
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
