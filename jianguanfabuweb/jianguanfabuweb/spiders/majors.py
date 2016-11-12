# -*- coding: utf-8 -*-
import scrapy
from jianguanfabuweb.items import MajorItem

class MajorsSpider(scrapy.Spider):
    name = "majors"
    allowed_domains = ["210.12.219.18"]
    start_urls = (
        'http://210.12.219.18/jianguanfabuweb/certifiedEngineers.html',
    )
    custom_settings = {
        'FEED_URI': 'outputs/majors.json',
        'FEED_FORMAT': 'json',
        'ITEM_PIPELINES': {
            'jianguanfabuweb.pipelines.AllowMajorPipeline': 100
        }
    }

    def __init__(self, start_url=None, *args, **kwargs):
        super(MajorsSpider, self).__init__(*args, **kwargs)
        pass

    def parse(self, response):
        options = response.css('#major option')
        for op in options:
            item = MajorItem()
            item['id'] = op.css('::attr(value)').extract_first()
            item['name'] = op.css('::text').extract_first()
            yield item
