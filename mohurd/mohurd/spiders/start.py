# -*- coding: utf-8 -*-

import re
from math import ceil
import urllib
import scrapy
from scrapy.http import Request

from mohurd.items import CompanyItem


class StartSpider(scrapy.Spider):
    name = 'start'
    start_urls = ['http://jzsc.mohurd.gov.cn/dataservice/query/staff/list']
    custom_settings = {
        'FEED_URI': 'outputs/id-name.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORTERS': {
            'csv': 'mohurd.exporters.MyCsvItemExporter'
        }
    }

    exclude_types = [u'注册建造师']

    page_size = 45
    page_step = 45 / 15

    default_payload = {
        '$pg': 1,
        '$pgsz': page_size,
        'ry_reg_type': ''
    }

    def parse(self, response):
        # get all category
        types = filter(
            lambda t: t.css('::text').extract_first().strip() not in self.exclude_types,
            response.css('.dropdown-menu.staff_dropdown>li>a[data-value]')
        )
        self.default_payload['ry_reg_type'] = ','.join(t.css('::attr(data-value)').extract_first() for t in types)

        # generate all page request.
        total = int(response.css('[sf=pagebar]').re_first(r'tt:(\d+)'))
        max_steps = int(ceil(1.0 * total / self.page_size))
        for _ in range(max_steps):
            yield Request(
                url='http://jzsc.mohurd.gov.cn/dataservice/query/staff/list',
                method='POST',
                body=urllib.urlencode(self.default_payload),
                headers={
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                callback=self.parser_staff_list
            )
            self.default_payload['$pg'] += self.page_step
            break

    def parser_staff_list(self, response):
        # generate staff detail page request.
        for detail_path in response.css('.personal').xpath(
                '//a[contains(@href, "/dataservice/query/staff/staffDetail/")]/@href').extract():
            yield Request('http://jzsc.mohurd.gov.cn' + detail_path, callback=self.parse_staff)

    def parse_staff(self, response):
        company_sel = response.css('[data-qyid]')
        if company_sel:
            company_id = company_sel.css('::attr(data-qyid)').extract_first()
            company_name = company_sel.css('::text').extract_first().strip()
        else:
            regex = re.compile(ur"注册单位.*</span>(.*)</dt", re.DOTALL)
            company_id = None
            company_name = response.css('#regcert_tab').re_first(regex).strip()
        return CompanyItem(id=company_id, name=company_name)
