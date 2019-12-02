import tornado.ioloop
from tornado.gen import multi
from tornado.httpclient import HTTPClient
from tornado.httpclient import AsyncHTTPClient
from tornado.concurrent import Future

urls = ['http://fanyi.youdao.com/',
        'http://fanyi.youdao.com/',
        'http://fanyi.youdao.com/',
        'http://fanyi.youdao.com/',
        'http://fanyi.youdao.com/',
        'http://fanyi.youdao.com/']


# def synchronous_fetch(url):
#     http_client = HTTPClient()
#     response = http_client.fetch(url)
#     return response.body
# def test_synchronous_fetch():
#     for url in urls:
#         # print(tornado.ioloop.IOLoop.run_in_executor(synchronous_fetch(url)))
#         print(synchronous_fetch(url))

async def asynchronous_fetch(url):
    http_client = AsyncHTTPClient()
    response = await http_client.fetch(url)
    return response.body
async def test_asynchronous_fetch():
    responses = await multi([asynchronous_fetch(url) for url in urls])
    print(responses)
    return responses

# def async_fetch_manual(url):
#     http_client = AsyncHTTPClient()
#     my_future = Future()
#     fetch_future = http_client.fetch(url)
#     def on_fetch(f):
#         my_future.set_result(f.result().body)
#     fetch_future.add_done_callback(on_fetch)
#     return my_future
# def test_async_fetch_manual():
#     for url in urls:
#         print(async_fetch_manual(url))  # fuck, how to start this??
if __name__ == '__main__':
    # test_synchronous_fetch()
    # test_asynchronous_fetch()
    # test_async_fetch_manual()

    io_loop = tornado.ioloop.IOLoop.current()
    io_loop.run_sync(test_asynchronous_fetch)
