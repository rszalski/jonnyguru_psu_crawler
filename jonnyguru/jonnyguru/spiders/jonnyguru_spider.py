# -*- coding: utf-8 -*-
import scrapy


class JonnyguruSpider(scrapy.Spider):
    name = "jonnyguru"
    allowed_domains = ["jonnyguru.com"]
    # Starts at PSU Reviews
    start_urls = ['http://www.jonnyguru.com/modules.php?name=NDReviews&op=Review_Cat&recatnum=13']

    def parse(self, response):
        pass
