# -*- coding: utf-8 -*-
import scrapy

import re
from math import ceil
import urllib
import scrapy
from scrapy.http import Request

from mohurd.items import CompanyItem


class CompSpider(scrapy.Spider):
    name = "comp"
    allowed_domains = ["http://jzsc.mohurd.gov.cn/dataservice/query/comp/list"]
    start_urls = ['http://http://jzsc.mohurd.gov.cn/dataservice/query/comp/list/']

    custom_settings = {
        'FEED_URI': 'outputs/id-name.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORTERS': {
            'csv': 'mohurd.exporters.MyCsvItemExporter'
        }
    }

    page_size = 45
    page_step = 45 / 15

    default_payload = {
        '$pg': 1,
        '$pgsz': page_size,
    }

    def parse(self, response):
        # generate all page request.
        total = int(response.css('[sf=pagebar]').re_first(r'tt:(\d+)'))
        max_steps = int(ceil(1.0 * total / self.page_size))
        for _ in range(max_steps):
            self.default_payload['$pg'] += self.page_step
            yield Request(
                url='http://jzsc.mohurd.gov.cn/dataservice/query/comp/list',
                method='POST',
                body=urllib.urlencode(self.default_payload),
                headers={
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                callback=self.parse_comp_list
            )
            if _ == 4:
                break

    def parse_comp_list(self, response):
        # generate comp detail page request.
        for tr in response.css('.personal tr'):
            tr.css('.')
        for detail_path in response.css('.personal').xpath(
                '//a[contains(@href, "/dataservice/query/comp/compDetail/")]/@href').extract():
            # yield Request('http://jzsc.mohurd.gov.cn' + detail_path, callback=self.parse_comp)
            print(detail_path)

    def parse_comp(self, response):
        company_sel = response.css('[data-qyid]')
        if company_sel:
            company_id = company_sel.css('::attr(data-qyid)').extract_first()
            company_name = company_sel.css('::text').extract_first().strip()
        else:
            regex = re.compile(r"注册单位.*</span>(.*)</dt", re.DOTALL)
            company_id = None
            company_name = response.css('#regcert_tab').re_first(regex).strip()
        return CompanyItem(id=company_id, name=company_name)
