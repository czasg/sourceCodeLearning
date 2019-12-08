#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2009 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import asyncio
import tornado.escape
import tornado.ioloop
import tornado.locks
import tornado.web
import os.path
import uuid

from tornado.options import define, options, parse_command_line

define("port", default=8888, help="run on the given port", type=int)
define("debug", default=True, help="run in debug mode")
"""
同步和异步的概念描述的是用户线程与内核的交互方式：同步是指用户线程发起IO请求后需要等待或者轮询内核IO操作完成后才能继续执行；而异步是指用户线程发起IO请求后仍继续执行，当内核IO操作完成后会通知用户线程，或者调用用户线程注册的回调函数。

1.1版本允许多个HTTP请求复用一个TCP连接，以加快传输速度。

执行时机	                执行方法
RequestHandler 实例化	initialize
找到处理方法	            prepare
调用处理方法	            get/post/put/delete/……
请求处理完成	            on_finish

方法	用户
set_status	设置响应状态码
set_header	设置响应头
clear_header	清除已设置的响应头
write	设置响应内容
clear	清除已设置的响应头和响应正文
flush	输出已设置的响应内容
finish	结束此次请求
render	调用模板生成响应内容，并结束会话
redirect	重定向
"""

class MessageBuffer(object):
    def __init__(self):
        # cond is notified whenever the message cache is updated
        self.cond = tornado.locks.Condition()
        self.cache = []
        self.cache_size = 200  # 原来还是可以做缓存的. 控制队列大小的方式, [:] = [-max_size:]

    def get_messages_since(self, cursor):
        """Returns a list of messages newer than the given cursor.

        ``cursor`` should be the ``id`` of the last message received.
        """
        results = []
        for msg in reversed(self.cache):
            if msg["id"] == cursor:
                break
            results.append(msg)
        results.reverse()
        return results

    def add_message(self, message):
        self.cache.append(message)  # 缓存数据消息
        if len(self.cache) > self.cache_size:
            self.cache = self.cache[-self.cache_size :]
        self.cond.notify_all()  # 释放锁


# Making this a non-singleton is left as an exercise for the reader.
global_message_buffer = MessageBuffer()


class MainHandler(tornado.web.RequestHandler):
    def get(self):  # 这种单纯的返回网页, 不需要使用异步的流程嘛
        self.render("index.html", messages=global_message_buffer.cache)


class MessageNewHandler(tornado.web.RequestHandler):
    """Post a new message to the chat room."""

    def post(self):
        message = {"id": str(uuid.uuid4()), "body": self.get_argument("body")}
        # render_string() returns a byte string, which is not supported
        # in json, so we must convert it to a character string.
        message["html"] = tornado.escape.to_unicode(
            self.render_string("message.html", message=message)
        )
        print('MessageNewHandler', message)
        if self.get_argument("next", None):
            self.redirect(self.get_argument("next"))
        else:
            self.write(message)
        global_message_buffer.add_message(message)


class MessageUpdatesHandler(tornado.web.RequestHandler):
    """Long-polling request for new messages.

    Waits until new messages are available before returning anything.
    """

    async def post(self):
        cursor = self.get_argument("cursor", None)
        messages = global_message_buffer.get_messages_since(cursor)
        while not messages:
            # Save the Future returned here so we can cancel it in
            # on_connection_close.
            self.wait_future = global_message_buffer.cond.wait()
            try:
                await self.wait_future
            except asyncio.CancelledError:
                return
            messages = global_message_buffer.get_messages_since(cursor)
        if self.request.connection.stream.closed():
            return
        # import time
        # time.sleep(10)
        print('MessageUpdatesHandler', messages)
        self.write(dict(messages=messages))  # 这个后端写的就很神奇了. 新用户建立连接就会完整的发送一份. 否则就发送最新的一条嘛

    def on_connection_close(self):
        self.wait_future.cancel()


def main():
    parse_command_line()
    app = tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/a/message/new", MessageNewHandler),
            (r"/a/message/updates", MessageUpdatesHandler),
        ],
        cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        xsrf_cookies=True,
        # debug=options.debug,
    )
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
