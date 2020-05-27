# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 20:34:07 2020

@author: Abhieshree Dhami
"""

import scrapy
from tripadvisorcrawler.items import ReviewItem
from scrapy import Request
 
class TripadvisorSpider(scrapy.Spider):
    name = "tripadvisor"
    start_urls = [
        "https://www.tripadvisor.com/Hotels-g187879-Sardinia-Hotels.html"]
    pages = 0
    #function to parse single review and save the data
    def parse_review(self, response):
        item = ReviewItem()
        item['reviewtitle'] = response.xpath('//h1[@id="HEADING"]/text()').extract()[0] #strip the quotes (first and last char)
        item['reviewcontent'] = response.xpath('//span[@class="fullText "]/text()').extract()[0]
        item['hotelname'] = response.xpath('//a[@class="ui_header h2"]/text()').extract()[0]
        var = response.xpath('//div[@class="reviewSelector"]//span[contains(@class, "ui_bubble_rating")]/@class').extract()[0]
        item['rating'] = var.split("_")[-1]  #to split the number/the rating from the html text
        yield item
    
    #scrapping the full review page by giving the pagination
    def parse_hotel(self, response):
        for href in response.xpath('//div[@class="location-review-review-list-parts-ReviewTitle__reviewTitle--2GO9Z"]/a/@href'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_review)
            
    
        next_page = response.xpath('//div[contains(@class,"ui_pagination")]/child::*[2][self::a]/@href')
        if next_page:
            url = response.urljoin(next_page[0].extract())
            yield scrapy.Request(url, self.parse_hotel)
            
    #main function to start at main page of sardinia hotels and scrap all the reviews for each hotel     
    def parse(self, response):
        urls=[]
        for href in response.xpath('//div[@class="listing_title"]/a/@href'):
            url = response.urljoin(href.extract())
            if url not in urls:
                urls.append(url)
                yield scrapy.Request(url, callback=self.parse_hotel)
 
        next_page = response.xpath('//div[contains(@class,"unified ui_pagination standard_pagination")]/child::*[2][self::a]/@href')
        if next_page:
            if self.pages<49:
                self.pages += 1
                url = response.urljoin(next_page[0].extract())
                yield scrapy.Request(url, self.parse)