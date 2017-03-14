# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class HospitalItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = Field()
    province = Field()
    city = Field()
    district = Field()
    address = Field()
    phone = Field()
    category = Field()
    label = Field()
    groundpos = Field()
    marspos = Field()
    baidupos = Field()
