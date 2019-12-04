# def gen_data():
#     total = 0
#     count = 0
#     data = True
#     while data:
#         data = yield data
#         total += data
#         count += 1
#     return total / count
#
#
#
# def middle(result, key):
#     while True:
#         result[key] = yield from gen_data()
#
#
# def main(data):
#     result = {}
#     for key, value in data.items():
#         mid = middle(result, key)
#         mid.send(None)
#
#
# if __name__ == '__main__':
#     data = {
#         'cza': [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 222, 3345]
#     }
#     main(data)

import _asyncio
import asyncio
from contextvars import ContextVar
async def test1():
    await asyncio.sleep(2)
    print('???')
    import time
    time.sleep(3)
    print('hahaha')
async def test2():
    await asyncio.sleep(3)
    print('???')
loop = asyncio.get_event_loop()
task1 = _asyncio.Task(test1(), loop=loop)
task2 = _asyncio.Task(test2(), loop=loop)
loop.run_until_complete(asyncio.wait([task1, task2]))



