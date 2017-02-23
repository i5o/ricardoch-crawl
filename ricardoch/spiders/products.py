# -*- coding: utf-8 -*-
# This runs in python 2

from urllib import unquote
from scrapy import Spider
from scrapy import Request
from scrapy.loader import ItemLoader
from ricardoch.items import Product


class ProductsSpider(Spider):
    name = "products"
    current_products = 0
    downloaded = 0

    def __init__(self):
        self.search_term = raw_input("Search term: ")
        self.max_products = int(
            raw_input("Products to download (int): ").strip())
        self.min_price = int(raw_input("Min price (int): ").strip())
        self.max_price = int(raw_input("Max price (int, 0 for no limit): ").strip())

    def start_requests(self):
        website_url = "https://www.ricardo.ch/search/index/?SearchSentence=%s&PageSize=120&PriceMin=%d" % (self.search_term, self.min_price)
        if self.max_price:
            website_url = "https://www.ricardo.ch/search/index/?SearchSentence=%s&PageSize=120&PriceMin=%d&PriceMax=%d" % (self.search_term, self.min_price, self.max_price)
        yield Request(url=website_url, callback=self.parse)

    def parse(self, response):
        products_url = response.xpath(
            '//li[@class="container-fluid"]/a/@href').extract()

        for product_url in products_url:
            product_link = "https://ricardo.ch" + product_url

            self.current_products += 1
            if self.current_products > self.max_products:
                return

            yield Request(url=product_link, callback=self.parse_product_data)

        next_url = response.xpath('//a[@data-track="Next"]/@href').extract()[0]
        print "-> Next page"
        yield Request(url="https://ricardo.ch" + next_url, callback=self.parse)

    def parse_product_data(self, response):
        self.downloaded += 1

        product_title = response.xpath(
            "//h1[@data-qa='title']/text()").extract()

        product_price = response.xpath(
            "//span[@itemprop='price']/text()").extract()
        if not len(product_price):
            product_bid = response.xpath(
                "//span[@data-qa='bidprice']/text()").extract()
            if len(product_bid):
                product_price = product_bid[0].strip()
            else:
                product_price = ""

        product_description_text = set(response.xpath(
            "//span[@itemprop='description']//text()").extract())

        product_description = ""
        for description_text in product_description_text:
            if description_text.strip():
                product_description += description_text
                product_description += "\n"

        product_number = response.url.split('/')[-2]

        product_image_urls = []
        for url in response.xpath(
                "//img[@class='ric-active']//@src").extract():
            full_url = "https:" + url
            full_url = unquote(full_url)
            full_url = full_url.replace(" ", "")
            product_image_urls.append(full_url)

        item = ItemLoader(item=Product(), response=response)
        item.add_value('title', product_title)
        item.add_value('description', product_description)
        item.add_value('price', product_price)
        item.add_value('number', product_number)
        item.add_value('image_urls', product_image_urls)
        item.add_value('search_term', self.search_term)

        item_loaded = item.load_item()
        print "product %s data downloaded (%d / %d)" % (product_number, self.downloaded, self.max_products)
        return item_loaded
