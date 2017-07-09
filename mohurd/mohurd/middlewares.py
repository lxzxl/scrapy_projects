# -*- coding: utf-8 -*-

import logging
from redis import StrictRedis

PROXY_SET = 'hq-proxies:proxy_pool'

logger = logging.getLogger(__name__)


class DynamicProxyMiddleware(object):
    def __init__(self, settings):
        self.redis_db = StrictRedis(
            host='127.0.0.1',
            port=6379,
            password='test',
            db=0
        )
        self.retry_http_codes = set(int(x) for x in settings.getlist('RETRY_HTTP_CODES'))

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_request(self, request, spider):
        proxy = self.redis_db.srandmember(PROXY_SET)
        print('使用代理[%s]访问[%s]' % (proxy, request.url))
        request.meta['proxy'] = proxy

    def process_response(self, request, response, spider):
        if response.status in self.retry_http_codes:
            self.redis_db.srem(PROXY_SET, request.meta.get('proxy', False))
        return response
