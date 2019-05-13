# -*- coding: utf-8 -*-
import scrapy
import socket
import datetime
import urllib.parse as urlparse
from videodifference.items import VideodifferenceItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join

def remove_blank(l):
	newlist = []
	for item in l:
		if item != "":
			newlist.append(item)
	return newlist

def valid_url(l):
	newlist = []
	for item in l:
		if item[:8] == "https://":
			newlist.append(item)
	return newlist

def valid_img(l):
	newlist = []
	for item in l:
		if item[:11] == "https://pic":
			newlist.append(item)
	return newlist

class BasicSpider(scrapy.Spider):
    name = 'basic'
    allowed_domains = ['web']
    start_urls = ['https://www.iqiyi.com/playlist553990602.html']

    def parse(self, response):
    	"""
        @url https://www.iqiyi.com/playlist553990602.html
        @returns items 1
        @scrapes title description more_links images_links
        @scrapes url project spider server date
        """

    	il = ItemLoader(item=VideodifferenceItem(), response=response)
    	mc = MapCompose(lambda i: urlparse.urljoin(response.url, i))

    	il.add_xpath('title', '//meta[@name="title"]/@content')
    	il.add_xpath('description', '//meta[@name="description"]/@content')
    	il.add_xpath('more_links', '//*[@class="link-txt"]/@href', mc, valid_url)
    	il.add_xpath('images_links', '//img/@src', mc, valid_img)

    	il.add_value('url', response.url)
    	il.add_value('project', self.settings.get('BOT_NAME'))
    	il.add_value('spider', self.name)
    	il.add_value('server', socket.gethostname())
    	il.add_value('date', datetime.datetime.now())

    	return il.load_item()
   	








