# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request
from ricardoch import settings
import os


class ProductImage(ImagesPipeline):

    def file_path(self, request, response=None, info=None):
        term_path = os.path.join(
            settings.DATA_STORE,
            request.meta["search_term"][0])
        data_path = os.path.join(term_path, request.meta["number"][0])
        if not os.path.exists(data_path):
            os.makedirs(data_path)

        filename = request.url.split("/")[-1]
        return os.path.join(request.meta["search_term"][0],
                            request.meta["number"][0], filename) + ".jpg"

    def get_media_requests(self, item, info):
        for url in item.get('image_urls'):
            yield Request(url, meta=item)

    def item_completed(self, results, item, info):
        item['images'] = [x for ok, x in results if ok]
        return item


class ProductText(object):

    def process_item(self, item, spider):
        term_path = os.path.join(settings.DATA_STORE, item["search_term"][0])
        data_path = os.path.join(term_path, item["number"][0])
        if not os.path.exists(data_path):
            os.makedirs(data_path)

        data_txt = "Title: %s\nDesc: %s\nPrice: %s" % (item["title"][0],
                                                       item["description"][0],
                                                       item["price"][0])

        file_path = os.path.join(data_path, "file")
        data_file = open(file_path, 'w')
        data_file.write(data_txt.encode('utf-8'))
        data_file.close()

        return item
