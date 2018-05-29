# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html


from scrapy import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst


class CompanyItem(Item):
    # define the fields for your item here like:
    area = Field(
        display_name='地区'
    )
    name = Field(
        display_name='名称'
    )
    domains = Field(
        display_name='专业范围',
    )
    address = Field(
        display_name='营业地址',
    )
    contact = Field(
        display_name='联系人',
    )
    phone = Field(
        display_name='联系电话',
    )

