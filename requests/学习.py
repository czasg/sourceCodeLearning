import socket
import time
import logging
import asyncio
import aiohttp
from concurrent import futures
from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ
selector = DefaultSelector()
stopped = False
urls_todo = {'/', '/1', '/2', '/3', '/4', '/5', '/6', '/7', '/8', '/9'}
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def blocking_way():
    sock = socket.socket()
    sock.connect(('www.baidu.com', 80))
    request = b'GRT / HTTP/1.0\r\n\r\n'
    sock.send(request)
    response = b''
    chunk = sock.recv(1024)
    while chunk:
        response += chunk
        chunk = sock.recv(1024)
    return response
# print(blocking_way())
def process_way():
    works = 10
    with futures.ProcessPoolExecutor(works) as executor:
        futs = {executor.submit(blocking_way) for _ in range(10)}
    return len([fut.result for fut in futs])
def thread_way():
    works = 10
    with futures.ThreadPoolExecutor(works) as executor:
        futs = {executor.submit(blocking_way) for _ in range(10)}
    return len([fut.result() for fut in futs])


def nonblocking_way():
    sock = socket.socket()
    sock.setblocking(False)
    try:
        sock.connect(('www.baidu.com', 80))
    except BlockingIOError:
        pass
    req = b'GET / HTTP/1.0\r\n\r\n'
    while True:
        try:
            sock.send(req)
            break
        except OSError:
            pass
    res = b''
    while True:
        try:
            chunk = sock.recv(1024)
            while chunk:
                res += chunk
                chunk = sock.recv(1024)
            break
        except OSError:
            pass
    return res


class Crawler:
    def __init__(self, url):
        self.url = url
        self.sock = None
        self.response = b''
    def fetch(self):
        self.sock = socket.socket()
        self.sock.setblocking(False)
        try:
            self.sock.connect(('www.baidu.com', 80))
        except BlockingIOError:
            pass
        selector.register(self.sock.fileno(), EVENT_WRITE, self.connected)
    def connected(self, key, mask):
        selector.unregister(key.fd)
        get = f'GET {self.url} HTTP/1.0\r\n\r\n'
        self.sock.send(get.encode('ascii'))
        selector.register(key.fd, EVENT_READ, self.read_response)
    def read_response(self, key, mask):
        global stopped
        chunk = self.sock.recv(1024)  # if size > 1024, next loop will still go here
        if chunk:
            self.response += chunk
        else:
            print(self.response)
            selector.unregister(key.fd)
            urls_todo.remove(self.url)
            if not urls_todo:
                stopped = True
def loop_main():
    for url in urls_todo:
        Crawler(url).fetch()
    while not stopped:
        test = selector.select()
        for key, mask in test:
            cb = key.data
            cb(key, mask)
# loop_main()

class Feature:
    def __init__(self):
        self.result = None
        self._callbacks = []
    def add_done_callback(self, fn):
        self._callbacks.append(fn)

    def set_result(self, result):
        self.result = result
        for fn in self._callbacks:
            fn(self)
class Crawler1:
    def __init__(self, url):
        self.url = url
        self.response = b''
    def fetch(self):
        sock = socket.socket()
        sock.setblocking(False)
        try:
            sock.connect(('www.baidu.com', 80))
        except BlockingIOError:
            pass
        f = Feature()
        def on_connected():
            logger.error(f'这个呢，谁先执行-{time.time()}')
            f.set_result(None)
        selector.register(sock.fileno(), EVENT_WRITE, on_connected)
        yield f
        logger.error(f'这个应该在后面执行-{time.time()}')
        selector.unregister(sock.fileno())
        get = f'GET {self.url} HTTP/1.0\r\n\r\n'
        sock.send(get.encode('ascii'))
        global stopped
        while True:
            f = Feature()
            def on_readable():
                f.set_result(sock.recv(1024))
            selector.register(sock.fileno(), EVENT_READ, on_readable)

            chunk = yield f
            selector.unregister(sock.fileno())
            if chunk:
                self.response += chunk
            else:
                logger.error(f'{self.response}')
                stopped = True
                # urls_todo.remove(self.url)
                # if not urls_todo:
                #     stopped = True
                # break
class Task:
    def __init__(self, coro):
        self.coro = coro
        f = Feature()
        f.set_result(None)
        self.step(f)
    def step(self, future):
        try:
            logger.error(f'显然这里会执行多变-{time.time()}')
            next_future = self.coro.send(future.result)
        except StopIteration:
            return
        next_future.add_done_callback(self.step)
def loop():
    while not stopped:
        events = selector.select()
        for key, mask in events:
            callback = key.data
            logger.error(f'{callback}')
            callback()
def loop_main1():
    import time
    start = time.time()
    Task(Crawler1('/').fetch())
    loop()
    print(time.time()-start)
# loop_main1()






def read(sock):
    f = Future()
    def on_readable():
        f.set_result(sock.recv(1024))
    selector.register(sock.fileno(), EVENT_READ, on_readable)
    chunk = yield from f
    selector.unregister(sock.fileno())
    return chunk
def read_all(sock):
    response = ['']
    chunk = yield from read(sock)
    while chunk:
        response.append(chunk)
        chunk = yield from read(sock)
    logger.error(f'{response}-这里是空的吗')
    return ''.join(response).encode()
def connect(sock, address):
    sock.setblocking(False)
    try:
        sock.connect(address)
    except BlockingIOError:
        pass
    f = Future()
    def on_connected():
        f.set_result(None)
    selector.register(sock.fileno(), EVENT_WRITE, on_connected)
    yield f
    selector.unregister(sock.fileno())
class Crawler2:
    def __init__(self, url):
        self.url = url
        self.response = b''
    def fetch(self):
        global stopped
        sock = socket.socket()
        yield from connect(sock, ('www.baidu.com', 80))
        get = 'GET / HTTP/1.0\r\n\r\n'
        sock.send(get.encode('ascii'))
        self.response = yield from read_all(sock)
        logger.error(f'{self.response}')
        stopped = True
class Future:
    def __init__(self):
        self.result = None
        self._callback = []
    def add_done_callback(self, fn):
        self._callback.append(fn)
    def set_result(self, result):
        for fn in self._callback:
            fn(self)
    def __iter__(self):
        yield self
        return self.result
def loop_main2():
    Task(Crawler2('/').fetch())
    loop()
# loop_main2()  # todo 返回值是空，这是为啥



def loop_main3():
    url = 'http://www.baidu.com'
    async def fetch(url):
        async with aiohttp.ClientSession(loop=loop) as session:
            async with session.get(url) as response:
                response = await response.read()
                return response
    loop = asyncio.get_event_loop()
    print(loop.run_until_complete(fetch(url)))
loop_main3()
