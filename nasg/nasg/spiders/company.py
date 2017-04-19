# -*- coding: utf-8 -*-
import scrapy


class CompanySpider(scrapy.Spider):
    name = "company"
    allowed_domains = ["http://chzz.nasg.gov.cn/UnitQuery.aspx"]
    start_urls = ['http://http://chzz.nasg.gov.cn/UnitQuery.aspx/']

    def parse(self, response):
        pass
