# -*- coding: utf-8 -*-

import os
import json
import urlparse
from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector

from jianguanfabuweb.items import UserLinkItem


class UserListSpider(CrawlSpider):
    name = "user_list"
    allowed_domains = ["210.12.219.18"]
    custom_settings = {
        'ITEM_PIPELINES': {
            'jianguanfabuweb.pipelines.CsvExportPipeline': 900
        }
    }

    page_size = 500
    base_path = 'http://210.12.219.18/jianguanfabuweb/handler/GetCompanyData.ashx' \
                '?method=GetEngineersData&name=&card=&stampnum=&company=' \
                '&major={major_id}&PageIndex={page_index}&PageSize=' + str(page_size)

    def __init__(self, start_url=None, *args, **kwargs):
        super(UserListSpider, self).__init__(*args, **kwargs)

        self.majors_mapping = self.get_major_mapping()
        if start_url:
            self.start_urls = (start_url,)
        else:
            self.start_urls = (self.base_path.format(major_id=major_id, page_index=1) for major_id in self.majors_mapping.keys())

    @staticmethod
    def get_major_mapping():
        root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
        with open(os.path.join(root, 'outputs/majors.json')) as fp:
            majors = json.load(fp)
        return {major['id']: major for major in majors}

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, headers={'Referer': 'http://210.12.219.18/jianguanfabuweb/certifiedEngineers.html'})

    def parse(self, response):
        try:
            jsonresponse = json.loads(response.body_as_unicode())
            # add more user list link
            query = urlparse.urlparse(response.request.url).query
            query_dict = urlparse.parse_qs(query)
            major_id = query_dict['major'][0]
            page_index = int(jsonresponse['PageIndex'])
            while page_index < int(jsonresponse['PageCount']):
                page_index += 1
                yield Request(self.base_path.format(major_id=major_id, page_index=page_index), headers={
                    'Referer': 'http://210.12.219.18/jianguanfabuweb/certifiedEngineers.html'
                })

            # parse detail link
            for href in Selector(text=jsonresponse['tb']).css('a::attr(href)').extract():
                yield UserLinkItem(major_id=major_id, url=href)
        except Exception as e:
            pass
