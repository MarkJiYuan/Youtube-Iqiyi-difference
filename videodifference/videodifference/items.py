# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

'测试用'
class VideodifferenceItem(Item):
    # Primary fields
    title = Field()
    description = Field()
    more_links = Field()
    images_links = Field()
    html_body = Field()

    # Calculated fields
    images = Field()
    location = Field()

    # Housekeeping fields
    url = Field()
    project = Field()
    spider = Field()
    server = Field()
    date = Field()

















