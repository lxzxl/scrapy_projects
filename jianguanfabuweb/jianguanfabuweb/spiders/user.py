# -*- coding: utf-8 -*-
import os
import json
import csv
from scrapy.http import Request
from scrapy.spiders import CrawlSpider

from jianguanfabuweb.items import UserItem, UserItemLoader


class UserSpider(CrawlSpider):
    name = "user"
    allowed_domains = ["210.12.219.18"]

    root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    custom_settings = {
        'JOBDIR': os.path.join(root_path, 'job_dir'),
        'ITEM_PIPELINES': {
            'jianguanfabuweb.pipelines.CsvExportPipeline': 900
        }
    }

    def __init__(self, start_url=None, *args, **kwargs):
        super(UserSpider, self).__init__(*args, **kwargs)

        self.majors_mapping = self.get_major_mapping()
        if start_url:
            self.start_urls = (start_url,)
        else:
            self.start_urls = self.get_urls()

    @classmethod
    def get_major_mapping(cls):
        with open(os.path.join(cls.root_path, 'outputs/majors.json')) as fp:
            majors = json.load(fp)
        return {major['id']: major for major in majors}

    @classmethod
    def get_urls(cls):
        with open(os.path.join(cls.root_path, 'outputs/user_list.csv')) as fp:
            for d in csv.DictReader(fp):
                yield 'http://210.12.219.18/jianguanfabuweb/' + d['url'], d['major_id']

    def start_requests(self):
        for url, major_id in self.start_urls:
            yield Request(url=url, meta={'major': self.majors_mapping[major_id]['name']})

    def parse(self, response):
        l = UserItemLoader(item=UserItem(), response=response)
        major = response.meta['major']
        l.add_value('major', major)
        l.add_css('name', '.engineer_basic_infor_table_name::text')
        for zs in response.css('.zhengshu'):
            if (major == zs.css('.zhengshu_head::text').extract_first().strip()):
                l.add_value('company', zs.css('.zhengshu_table_company_name>a::text').extract_first())
                break
        return l.load_item()
