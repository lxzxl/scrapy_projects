# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class StaffItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = Field(
        display_name='编号'
    )
    name = Field(
        display_name='姓名'
    )
    company_id = Field(
        display_name='单位编号'
    )


class CompanyItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = Field(
        display_name='编号'
    )
    name = Field(
        display_name='单位名称'
    )
