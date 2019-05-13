# -*- coding: utf-8 -*-
import scrapy


class FunvideoSpider(scrapy.Spider):
    name = 'funvideo'
    allowed_domains = ['web']
    start_urls = ['http://web/']

    def parse(self, response):
        pass
