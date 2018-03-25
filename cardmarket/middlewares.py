import random
from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware


class RotateUserAgentMiddleware(UserAgentMiddleware):

    def __init__(self, user_agent=''):
        self.user_agent = user_agent

    def process_request(self, request, spider):
        ua = random.choice(spider.settings.get('USER_AGENT_LIST'))
        if ua:
            request.headers.setdefault('User-Agent', ua)


class TorProxyMiddleware(object):

    def process_request(self, request, spider):
        request.meta['proxy'] = 'http://127.0.0.1:8123'
