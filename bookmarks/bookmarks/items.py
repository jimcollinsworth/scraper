# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookmarksItem(scrapy.Item):
    url = scrapy.Field()
    status = scrapy.Field()
    title = scrapy.Field()
    
