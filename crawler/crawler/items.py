# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XMLItem(scrapy.Item):
    xml = scrapy.Field()
    meta = scrapy.Field()
    url = scrapy.Field()
