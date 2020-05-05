# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html


import scrapy


class ReviewItem(scrapy.Item):
    # Items to get
    
    reviewcontent = scrapy.Field()
    reviewtitle = scrapy.Field()
    rating = scrapy.Field()
    hotelname = scrapy.Field()
    #url = scrapy.Field()

