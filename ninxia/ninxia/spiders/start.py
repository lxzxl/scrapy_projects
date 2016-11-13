# -*- coding: utf-8 -*-

import urllib
import urlparse

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request

from ninxia.items import UserItem, UserItemLoader


class StartSpider(CrawlSpider):
    name = 'start'
    allowed_domains = ['61.133.208.18']
    start_urls = [
        'http://61.133.208.18:8089/jgpt/zcd/web/qyxx/qyjbxxList.jsp'
    ]

    rules = (
        Rule(LinkExtractor(allow=r'qyxx.jsp'), callback='parse_item'),
    )

    custom_settings = {
        'FEED_URI': 'outputs/users.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORTERS': {
            'csv': 'ninxia.exporters.MyCsvItemExporter'
        }
    }

    def start_requests(self):
        payload = {
            'wherestr': "",
            'wherepre': " and ( t.blzt='1' and t.shzt='1' and t.sfwlqy in ('F','T') and b.zzlx in ('Z101','Z102','Z103','Z104','Z105','Z106','Z107','Z108','Z120','Z199'))",
            'sfwlqy': "('F','T')",
            'zzlx': "('Z101','Z102','Z103','Z104','Z105','Z106','Z107','Z108','Z120','Z199')",
            'pagerec': 15,
            'pageno': 1
        }
        for i, url in enumerate(self.start_urls):
            yield Request(
                url=url,
                method='POST',
                body=urllib.urlencode(payload),
                headers={
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            )

    def parse_item(self, response):
        # get baisc info.
        l = UserItemLoader(item=UserItem(), response=response)
        l.add_xpath('phone', u'//*[@id="printTable"]//td[@title="{0}"]/text()'.format(UserItem.fields['phone']['html_title']))
        # query more detail info.
        query = urlparse.urlparse(response.request.url).query
        query_dict = urlparse.parse_qs(query)
        qyid = query_dict['qyid'][0]
        sfwlqy = query_dict['sfwlqy'][0]  # T(non-ninxia) or F(ninxia)
        detail_url = 'http://61.133.208.18:8089/jgpt/zcd/web/qyxx/qyjbxx.jsp?pid=123&qyid={0}'
        yield Request(
            url=detail_url.format(qyid),
            headers={
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            meta={
                'item': l.load_item(),
                'sfwlqy': sfwlqy
            },
            callback=self.parse_item_detail
        )

    def parse_item_detail(self, response):
        item = response.meta['item']
        sfwlqy = response.meta['sfwlqy']

        l = UserItemLoader(item, response=response)

        # both
        l.add_xpath('office_phone', u'//*[@id="printTable"]//td[@title="{0}"]/text()'.format(UserItem.fields['office_phone']['display_name']))
        l.add_xpath('fax', u'//*[@id="printTable"]//td[@title="{0}"]/text()'.format(UserItem.fields['fax']['display_name']))

        # F - ninxia
        if sfwlqy == 'F':
            l.add_value('type', u'区内')
            l.add_xpath('name', u'//*[@id="printTable"]//td[@title="{0}"]/text()'.format(UserItem.fields['name']['display_name']))
            l.add_xpath('address', u'//*[@id="printTable"]//td[@title="{0}"]/text()'.format(UserItem.fields['address']['display_name']))
            l.add_xpath('contact_name', u'//*[@id="printTable"]//td[@title="{0}"]/text()'.format(UserItem.fields['contact_name']['display_name']))
            l.add_xpath('contact_phone', u'//*[@id="printTable"]//td[@title="{0}"]/text()'.format(UserItem.fields['contact_phone']['display_name']))
            l.add_xpath('contact_office_phone',
                        u'//*[@id="printTable"]//td[@title="{0}"]/text()'.format(UserItem.fields['contact_office_phone']['display_name']))
        # T - non-ninxia
        elif sfwlqy == 'T':
            l.add_value('type', u'进宁')
            l.add_xpath('name', u'//*[@id="printTable"]//td[@title="{0}"]/text()'.format(UserItem.fields['name']['display_name']))
            l.add_xpath('name_sub', u'//*[@id="printTable"]//th[.="{0}"]/following-sibling::td[1]/text()'.format(UserItem.fields['name_sub']['display_name']))

        return l.load_item()
