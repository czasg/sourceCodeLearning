import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        greeting = self.get_argument('greeting', 'Hello')
        self.write(greeting + ', friendly user!')

if __name__ == "__main__":
    # tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/", IndexHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

"""
Web框架
主要包括RequestHandler用于创建Web应用程序和各种支持类的子类
HTTP服务器与客户端
主要包括HTTPServer和AsyncHTTPClient
异步网络库
主要包括IOLoop和IOStream作为HTTP组件的构建块

Tornado服务器的三个底层核心模块
httpserver 服务于web模块的一个简单的HTTP服务器的实现
Tornado的HTTPConnection类用来处理HTTP请求，包括读取HTTP请求头、读取POST传递的数据，调用用户自定义的处理方法，以及把响应数据写给客户端的socket。
iostream 对非阻塞式的socket的封装以便于常见读写操作
为了在处理请求时实现对socket的异步读写，Tornado实现了IOStream类用来处理socket的异步读写。
ioloop 核心的I/O循环
Tornado为了实现高并发和高性能，使用了一个IOLoop事件循环来处理socket的读写事件，IOLoop事件循环是基于Linux的epoll模型，可以高效地响应网络事件，这是Tornado高效的基础保证。
"""
