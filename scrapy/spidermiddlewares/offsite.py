"""
Offsite Spider Middleware

See documentation in docs/topics/spider-middleware.rst
"""
import re
import logging
import warnings

from scrapy import signals
from scrapy.http import Request
from scrapy.utils.httpobj import urlparse_cached

logger = logging.getLogger(__name__)


class OffsiteMiddleware(object):
    """
    这玩意原来是一个统计过滤以及执行allowed_domains过滤的地方
    """

    def __init__(self, stats):
        self.stats = stats

    @classmethod
    def from_crawler(cls, crawler):
        o = cls(crawler.stats)
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        return o

    def process_spider_output(self, response, result, spider):
        for x in result:
            if isinstance(x, Request):
                if x.dont_filter or self.should_follow(x, spider):
                    yield x  # 如果指定了dont_filter，或者该Request符合allowed_domains。则可以通过
                else:
                    domain = urlparse_cached(x).hostname
                    if domain and domain not in self.domains_seen:
                        self.domains_seen.add(domain)
                        logger.debug(
                            "Filtered offsite request to %(domain)r: %(request)s",
                            {'domain': domain, 'request': x}, extra={'spider': spider})
                        self.stats.inc_value('offsite/domains', spider=spider)
                    self.stats.inc_value('offsite/filtered', spider=spider)
            else:
                yield x

    def should_follow(self, request, spider):
        regex = self.host_regex
        # hostname can be None for wrong urls (like javascript links)
        host = urlparse_cached(request).hostname or ''
        return bool(regex.search(host))

    def get_host_regex(self, spider):
        """Override this method to implement a different offsite policy"""
        allowed_domains = getattr(spider, 'allowed_domains', None)
        if not allowed_domains:
            return re.compile('')  # allow all by default
        url_pattern = re.compile("^https?://.*$")
        for domain in allowed_domains:
            if url_pattern.match(domain):
                message = ("allowed_domains accepts only domains, not URLs. "
                           "Ignoring URL entry %s in allowed_domains." % domain)
                warnings.warn(message, URLWarning)
        domains = [re.escape(d) for d in allowed_domains if d is not None]
        regex = r'^(.*\.)?(%s)$' % '|'.join(domains)
        return re.compile(regex)

    def spider_opened(self, spider):
        self.host_regex = self.get_host_regex(spider)
        self.domains_seen = set()


class URLWarning(Warning):
    pass


"""
OffsiteMiddleware
平常看到的统计过滤的，就是这里实现的
该中间件也是实现 allowed_domains 过滤的主要类
原来还统计了domains这个呀，可以的
"""
