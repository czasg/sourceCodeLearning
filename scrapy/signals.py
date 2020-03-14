"""coding: utf-8
Scrapy signals

These signals are documented in docs/topics/signals.rst. Please don't add new
signals here without documenting them there.
"""

engine_started = object()  # 引擎启动 - engine | def start(self):
engine_stopped = object()  # 引擎终止 - engine | def _finish_stopping_engine:
spider_opened = object()  # 爬虫初始化 - engine | def open_spider(self, spider, start_requests=(), close_if_idle=True):
spider_idle = object()  # 爬虫停歇 - engine | def _spider_idle(self, spider):
spider_closed = object()  # 爬虫关闭 - engine | def close_spider(self, spider, reason='cancelled'):
spider_error = object()  # 爬虫报错 - scraper | def handle_spider_error(self, _failure, request, response, spider):
request_scheduled = object()  # 请求调度 - engine | def schedule(self, request, spider):
request_dropped = object()  # 请求抛弃 - engine | def schedule(self, request, spider):
request_reached_downloader = object()  # 请求接触下载器 downloader | def _enqueue_request(self, request, spider):
response_received = object()  # 结果接收 engine | def _download(self, request, spider):
response_downloaded = object()  # 结果下载完毕 downloader | def _download(self, slot, request, spider):
item_scraped = object()  # 当前数据已处理完毕 scraper | def _itemproc_finished(self, output, item, response, spider):
item_dropped = object()  # 数据抛弃 scraper | def _itemproc_finished(self, output, item, response, spider):
item_error = object()  # 数据报错 scraper | def _itemproc_finished(self, output, item, response, spider):

# for backwards compatibility
stats_spider_opened = spider_opened
stats_spider_closing = spider_closed
stats_spider_closed = spider_closed

item_passed = item_scraped

request_received = request_scheduled


"""
signal机制贯穿整个scrapy框架，支撑整个extensions模块的运行，也就是拓展模块，是基于信号机制运行的。

"""