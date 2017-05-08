# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst
from w3lib.html import replace_entities


class UserItem(Item):
    # define the fields for your item here like:
    # basic info
    type = Field(
        display_name=u'公司类型'
    )
    phone = Field(
        display_name=u'联系电话',
        html_title=u'联系人手机号码'  # for output to avoid duplicate html_title
    )
    # detail page.
    name = Field(
        display_name=u'企业名称',
    )
    office_phone = Field(
        display_name=u'办公电话',
    )
    fax = Field(
        display_name=u'传真号码',
    )
    address = Field(
        display_name=u'营业地址',
    )
    contact_name = Field(
        display_name=u'联系人姓名',
    )
    contact_phone = Field(
        display_name=u'联系人手机号码',
    )
    contact_office_phone = Field(
        display_name=u'联系人办公电话',
    )
    name_sub = Field(
        display_name=u'分公司企业名称',
    )


class UserItemLoader(ItemLoader):
    default_input_processor = MapCompose(replace_entities, str.strip)
    default_output_processor = TakeFirst()
