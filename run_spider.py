# -*- coding: utf-8 -*-

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

import logging

print "-> Crawl started"
process = CrawlerProcess(get_project_settings())
logging.getLogger('scrapy').setLevel(logging.WARNING)
process.crawl('products')
process.start()
print "-> Crawl stopped"
