#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)


class MainHandler(tornado.web.RequestHandler):  # 感觉还是函数式编程友好一点啊，看着就舒服. 但是这种也感觉不错，针对各种请求有不同的方案清洗明了
    def get(self):
        self.write("Hello, world")


def main():
    # tornado.options.parse_command_line()
    application = tornado.web.Application(
        [(r"/", MainHandler)],  # url的映射关系. 后面其实还可以接一些初始化参数
    )
    http_server = tornado.httpserver.HTTPServer(application)  # 这是一种启动方式, 调用HttPServer
    http_server.listen(options.port)  # 监听端口
    tornado.ioloop.IOLoop.current().start()  # 启动异步轮询


if __name__ == "__main__":
    main()
