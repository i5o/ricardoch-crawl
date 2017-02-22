# -*- coding: utf-8 -*-

# Scrapy settings for ricardoch project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
import os
BOT_NAME = 'ricardoch'

SPIDER_MODULES = ['ricardoch.spiders']
NEWSPIDER_MODULE = 'ricardoch.spiders'

ITEM_PIPELINES = {'ricardoch.pipelines.ProductText': 0,
                  'ricardoch.pipelines.ProductImage': 1}

DATA_STORE = os.path.join(os.getcwd(), "Grabber")
IMAGES_STORE = DATA_STORE

if not os.path.exists(DATA_STORE):
    os.mkdir(DATA_STORE)

LOG_LEVEL = 'WARNING'

# Search term
SEARCH_TERM = "iphone"

# max products
MAX_PRODUCTS = 20
