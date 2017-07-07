# -*- coding: utf-8 -*-

from redis import StrictRedis

PROXY_SET = 'hq-proxies:proxy_pool'


class DynamicProxyMiddleware(object):
    def process_request(self, request, spider):
        redis_db = StrictRedis(
            host='127.0.0.1',
            port=6379,
            password='test',
            db=0
        )
        proxy = redis_db.srandmember(PROXY_SET)
        print('使用代理[%s]访问[%s]' % (proxy, request.url))
        request.meta['proxy'] = proxy
