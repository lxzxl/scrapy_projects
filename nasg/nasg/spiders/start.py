# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy.http import Request, FormRequest

from nasg.items import NasgItem, NasgItemLoader

regex = re.compile(r"((?P<id>\d+),(?P<level>\d+))")


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
            encoding='utf-8',
            callback=self.parse_page
        )

    def parse_page(self, response):
        # go to next page.
        total_page = 125
        formdata = {
            'ScriptManager1': 'UpdatePanel5|PageTurnControl1$ANPager',
            '__EVENTTARGET': 'PageTurnControl1$ANPager',
            '__EVENTARGUMENT': 1,
            '__VIEWSTATE': response.css('#__VIEWSTATE::attr(value)').extract_first() or '',
        }
        formdata['__EVENTARGUMENT'] += 1
        while formdata['__EVENTARGUMENT'] <= total_page:
            yield FormRequest(
                url='http://chzz.nasg.gov.cn/UnitQuery.aspx',
                formdata={k: str(v) for k, v in formdata.iteritems()},
                headers={
                    'X-MicrosoftAjax': 'Delta=true',
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
                },
                meta={
                    'page': formdata['__EVENTARGUMENT']
                },
                encoding='utf-8',
                callback=self.parser_special_list
            )
            formdata['__EVENTARGUMENT'] += 1

        # generate detail page request
        for R in self.parser_special_list(response):
            yield R

    def parser_special_list(self, response):
        page = 'page' in response.meta and response.meta['page'] or 1
        ids = response.css('table')[0].css('td.td[align=center]:nth-of-type(1)::text').extract()
        self.logger.info('Page %s: %s - %s', page, ids[0], ids[-1])
        for onclick in response.css('table')[0].css('a::attr(onclick)').extract():
            # ShowInfo(341,1)
            match = regex.search(onclick)
            if match:
                yield Request(
                    url='http://chzz.nasg.gov.cn/PorttalWeb/UnitBaseInfoView.aspx?ID={id}&Level={level}'.format(**match.groupdict()),
                    encoding='utf-8',
                    callback=self.parse_detail
                )

    def parse_detail(self, response):
        l = NasgItemLoader(item=NasgItem(), response=response)
        l.add_css('level', '#lblSurveyLevelType::text')
        l.add_css('name', '#lllName::text')
        l.add_css('address', '#lblOfficeAddress::text')
        l.add_css('zipcode', '#lblOfficePostCode::text')
        l.add_css('contact_name', '#lblContact::text')
        l.add_css('phone', '#lblTelNumber::text')
        l.add_css('cert_number', '#lblCertificateCode::text')
        return l.load_item()
