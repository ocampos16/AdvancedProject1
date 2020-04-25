# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ReviewItem(scrapy.Item):
    # Items to get
    hotelname = scrapy.Field()
    rating = scrapy.Field()
    reviewtitle = scrapy.Field()
    reviewcontent = scrapy.Field()
    