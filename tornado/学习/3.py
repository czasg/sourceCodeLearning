import errno
import functools
import socket

import tornado.ioloop
from tornado.iostream import IOStream


async def handle_connection(connection, address):
    stream = IOStream(connection)
    message = await stream.read_until_close()
    print("message from client:", message.decode().strip())


def connection_ready(sock, fd, events):
    while True:
        try:
            connection, address = sock.accept()
        except socket.error as e:
            if e.args[0] not in (errno.EWOULDBLOCK, errno.EAGAIN):
                raise
            return
        connection.setblocking(0)
        io_loop = tornado.ioloop.IOLoop.current()
        io_loop.spawn_callback(handle_connection, connection, address)


if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setblocking(0)
    sock.bind(("", 8888))
    sock.listen(128)

    io_loop = tornado.ioloop.IOLoop.current()  # 这个current => asyncio.get_event_loop()
    callback = functools.partial(connection_ready, sock)  # = > 初始化回调函数的一个值
    io_loop.add_handler(sock.fileno(), callback, io_loop.READ)  # selectors.register(fileno, READ, callback)
    # print(io_loop)  # <tornado.platform.asyncio.AsyncIOMainLoop object at 0x028ECCB0>
    io_loop.start()

# import typing
# class Test:
#     @typing.overload
#     def test(self, s: int) -> None:
#         a = 0
#         a += s
#         print(s)
#
#     @typing.overload
#     def test(self, s: str) -> None:
#         s = ""
#         s += s
#         print(s)
# ttt = Test()
# ttt.test(123)
# ttt.test("666")