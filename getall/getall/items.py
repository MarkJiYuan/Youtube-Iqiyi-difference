# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class GetallItem(Item):
   	
   	title = Field()
   	url = Field()
   	more_urls = Field()
   	html_body = Field()

