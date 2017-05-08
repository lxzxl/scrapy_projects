# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose


class MajorItem(Item):
    # define the fields for your item here like:
    id = Field()
    name = Field()


class UserLinkItem(Item):
    major_id = Field()
    url = Field()


def serialize_unicode(value):
    return value.encode('utf8')


class UserItem(Item):
    major = Field(serializer=serialize_unicode)
    name = Field(serializer=serialize_unicode)
    company = Field(serializer=serialize_unicode)


class UserItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    name_in = MapCompose(str.strip)
    company_in = MapCompose(str.strip)
