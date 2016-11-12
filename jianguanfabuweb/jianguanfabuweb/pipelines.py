# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from scrapy import signals
from scrapy.exporters import CsvItemExporter


class AllowMajorPipeline(object):
    allowed_majors = [u'二级注册建筑师', u'二级注册结构工程师', u'注册化工工程师', u'监理工程师', u'造价工程师'];

    def process_item(self, item, spider):
        # print item
        if item['name'] in self.allowed_majors:
            return item
        else:
            raise DropItem("Not needed major %s" % item['name'])


class CsvExportPipeline(object):
    def __init__(self):
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        fp = open('outputs/%s.csv' % spider.name, 'w+b')
        self.files[spider] = fp
        self.exporter = CsvItemExporter(fp)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        fp = self.files.pop(spider)
        fp.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
