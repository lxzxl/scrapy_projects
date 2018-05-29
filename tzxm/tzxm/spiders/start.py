# -*- coding: utf-8 -*-

import copy
import json
from urllib.parse import urlencode

import scrapy
from scrapy.http import Request

from ..items import CompanyItem

area_list = [
    ["110000", "北京市"],
    ["120000", "天津市"], ["130000", "河北省"], ["140000", "山西省"], ["150000", "内蒙古自治区"], ["210000", "辽宁省"],
    ["210200", "大连市"], ["220000", "吉林省"], ["230000", "黑龙江省"], ["310000", "上海市"], ["320000", "江苏省"], ["330000", "浙江省"],
    ["330200", "宁波市"], ["340000", "安徽省"], ["350000", "福建省"], ["350200", "厦门市"], ["360000", "江西省"], ["370000", "山东省"],
    ["370200", "青岛市"], ["410000", "河南省"], ["420000", "湖北省"], ["430000", "湖南省"], ["440000", "广东省"], ["440300", "深圳市"],
    ["450000", "广西自治区"], ["460000", "海南省"], ["510000", "四川省"], ["500000", "重庆市"], ["520000", "贵州省"], ["530000", "云南省"],
    ["540000", "西藏自治区"], ["610000", "陕西省"], ["620000", "甘肃省"], ["630000", "青海省"], ["640000", "宁夏自治区"],
    ["650000", "新疆自治区"], ["000015", "新疆生产建设兵团"]
]

base_url = 'https://www.tzxm.gov.cn:8081/tzxmspweb/projectConsultant.do?method='
list_url = base_url + 'getConsultantList'
info_url = base_url + 'getComPanyInfoList'


class StartSpider(scrapy.Spider):
    name = 'start'
    custom_settings = {
        'FEED_URI': 'outputs/all.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORTERS': {
            'csv': 'tzxm.exporters.MyCsvItemExporter'
        }
    }

    list_payload = {
        'dept_name': '',
        'area_code': '',
        'work_time': '',
        'consultant_num': 0,
        'ba_domian': '',
        'pageNo': 1,
        'pageSize': 100,
    }

    def start_requests(self):
        for code, _ in area_list:
            payload = copy.copy(self.list_payload)
            payload['area_code'] = code
            yield Request(
                list_url,
                method='POST',
                body=urlencode(payload),
                headers={
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                meta={
                    'payload': payload
                },
                callback=self.parse_start_response
            )

    def parse_start_response(self, response):
        data = json.loads(response.body_as_unicode())
        for r in self.parse_list_response(response):
            yield r
        payload = response.meta['payload']
        for page_num in range(2, data['PAGENUMS'] + 1):
            payload['pageNo'] = page_num
            yield Request(
                list_url,
                method='POST',
                body=urlencode(payload),
                headers={
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                callback=self.parse_list_response
            )

    def parse_list_response(self, response):
        data = json.loads(response.body_as_unicode())
        return self.parse_list_data(data)

    def parse_list_data(self, data):
        return self.generate_info_requests(data['DATA'])

    def generate_info_requests(self, data):
        # generate staff detail page request.
        for item in data:
            yield Request(
                info_url,
                method='POST',
                body=urlencode({'uuid': item['COMPANY_UUID']}),
                headers={
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                meta={
                    'area': item['AREA_CODE'],
                    'name': item['DEPT_NAME'],
                    'domains': item['BA_DOMAIN_TOOLTIP']
                },
                callback=self.parse_info
            )

    def parse_info(self, response):
        area = response.meta['area']
        name = response.meta['name']
        domains = response.meta['domains']
        data = json.loads(response.body_as_unicode())
        address = data['companyInfoList'][0]['contact_address']
        contact = data['companyContactList'][0]['name']
        phone = data['companyContactList'][0]['telephone']

        return CompanyItem(area=area, name=name, domains=domains, address=address, contact=contact, phone=phone)
