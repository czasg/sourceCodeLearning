import requests
# todo 能不能用asyncio搭建一个啊
class Base:
    url = None

    def start_requests(self):
        self.parse(requests.get(self.url))


    def parse(self, response):
        """Ni"""

