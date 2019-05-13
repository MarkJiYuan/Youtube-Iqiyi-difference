# -*- coding: utf-8 -*-
import scrapy
import urllib.parse as urlparse
import time
import random
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join
from getall.items import GetallItem

def valid_url(l):
	return [ url for url in l if url != '' and url != 'javascript:void(0);' ]

class BasicSpider(scrapy.Spider):
    name = 'basic'
    # allowed_domains = ['www.iqiyi.com']
    start_urls = [ url.strip() for url in open('more_urls.txt').readlines() if url.strip() != "javascript:;" ]

    def parse(self, response):
        il = ItemLoader(item=GetallItem(), response=response)

        il.add_xpath('title', '//title/text()')

        il.add_value('url', response.url)

        url_mc = MapCompose(lambda i: urlparse.urljoin(response.url, i))
        il.add_xpath('more_urls', '//a/@href', valid_url, url_mc)

        il.add_value('html_body', response.body.decode('utf-8'))

        time.sleep(random.randint(0,5))

        return il.load_item()