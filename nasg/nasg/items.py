# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst
from w3lib.html import replace_entities


class NasgItem(Item):
    # define the fields for your item here like:
    id = Field(
        display_name=u'单位编号',
    )
    level = Field(
        display_name=u'资质等级'
    )
    name = Field(
        display_name=u'单位名称',
    )
    address = Field(
        display_name=u'单位地址',
    )
    zipcode = Field(
        display_name=u'邮政编码',
    )
    contact_name = Field(
        display_name=u'联系人',
    )
    phone = Field(
        display_name=u'联系电话',
    )
    cert_number = Field(
        display_name=u'资质证号',
    )


class NasgItemLoader(ItemLoader):
    default_input_processor = MapCompose(replace_entities, str.strip)
    default_output_processor = TakeFirst()
