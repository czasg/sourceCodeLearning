import requests
# todo 能不能用asyncio搭建一个啊
class Base:
    url = None

    def start_requests(self):
        self.parse(requests.get(self.url))


    def parse(self, response):
        """Ni"""

import asyncio
import time

async def test1():
    time.sleep(5)
    print('test1')
async def test2():
    time.sleep(2)
    print('test2')
async def main():
    await asyncio.gather(test1(), test2())
import time
now = time.time()
asyncio.run(main())
print(time.time()-now)