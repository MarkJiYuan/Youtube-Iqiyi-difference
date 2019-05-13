# -*- coding: utf-8 -*-
import scrapy
import datetime
import socket
import urllib.parse as urlparse
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join
from videodifference.items import LevelOnePageItem


class LeveloneSpider(scrapy.Spider):
    name = 'levelone'
    allowed_domains = ['web']
    start_urls = ['https://www.iqiyi.com/']

    def parse(self, response):
        
        il = ItemLoader(item=LevelOnePageItem(), response=response)

        il.add_value('datetime', datetime.datetime.now())

        return il.load_item()