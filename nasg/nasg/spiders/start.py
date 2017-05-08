# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request, FormRequest

from nasg.items import NasgItem, NasgItemLoader


class NasgSpider(scrapy.Spider):
    name = "nasg"
    # allowed_domains = ["http://chzz.nasg.gov.cn/UnitQuery.aspx"]
    start_urls = ['http://chzz.nasg.gov.cn/UnitQuery.aspx']

    custom_settings = {
        'FEED_URI': 'outputs/id-level.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORTERS': {
            'csv': 'nasg.exporters.MyCsvItemExporter'
        }
    }

    default_payload = {
        'PageTurnControl1$SelectPageSize': 15,
        'PageTurnControl1$ANPager_input': 3,
        'PageTurnControl1$HiddenPageSize': 15,
    }

    def parse(self, response):
        yield FormRequest.from_response(
            response,
            formname='form1',
            callback=self.parse_page
        )

    def parse_page(self, response):
        # detail page.
        l = NasgItemLoader(item=NasgItem(), response=response)
        yield Request(
            url='',
            headers={
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            meta={
                'item': l.load_tems()
            },
            callback=self.parse_detail()
        )
        # go to next page.
        payload = {
            '__EVENTTARGET': response.selector.css('#__EVENTTARGET::attr(value)').extract_first(),
            '__EVENTARGUMENT': response.selector.css('#__EVENTARGUMENT::attr(value)').extract_first(),
            '__LASTFOCUS': response.selector.css('#__LASTFOCUS::attr(value)').extract_first(),
            '__VIEWSTATE': response.selector.css('#__VIEWSTATE::attr(value)').extract_first(),
            '__EVENTVALIDATION': response.selector.css('#__EVENTVALIDATION::attr(value)').extract_first(),
        }
        yield Request()

    def parse_partial_page(self, response):
        yield Request(
            url='',
            headers={
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            meta={
                'item': l.load_tems()
            },
            callback=self.parse_detail()
        )

    def parse_detail(self, response):
        item = response.meta['item']
        l = NasgItemLoader(item, response=response)
