# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Product(scrapy.Item):
    images = scrapy.Field()
    image_urls = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    bidprice = scrapy.Field()
    price = scrapy.Field()
    number = scrapy.Field()
    search_term = scrapy.Field()
