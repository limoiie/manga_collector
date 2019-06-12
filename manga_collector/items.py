# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MangaCollecterItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class MangaChapterItem(scrapy.Item):
    book = scrapy.Field()
    version = scrapy.Field()
    chapter_no = scrapy.Field()
    title = scrapy.Field()
    pages = scrapy.Field()
    chapter_url = scrapy.Field()
    store_dir = scrapy.Field()
