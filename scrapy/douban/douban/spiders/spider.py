#-*-coding:utf-8-*- 
__author__ = 'Administrator'

# import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from douban.items import DoubanItem


class Douban(CrawlSpider):
    name = 'douban'
    redis_key = 'douban:start_urls'
    start_urls = ["http://movie.douban.com/top250"]

    url = 'http://movie.douban.com/top250'

    def parse(self, response):
        item = DoubanItem()
        selector = Selector(response)
        movies = selector.xpath("//div[@class='item']")
        for eachmovie in movies:
            title = eachmovie.xpath('div[@class="info"]/div[@class="hd"]/a/span/text()').extract()
            name = ''
            for each in title:
                name += each
            id = eachmovie.xpath('div[@class="pic"]/em/text()').extract()[0]
            movieinfo = eachmovie.xpath('div[@class="info"]/div[@class="bd"]/p/text()').extract()
            star = eachmovie.xpath('div[@class="info"]/div[@class="bd"]/div[@class="star"]/span/em/text()').extract()[0]
            quote = eachmovie.xpath('div[@class="info"]/div[@class="bd"]/p[@class="quote"]/span/text()').extract()
            if quote:
                quote = quote[0]
            else:
                quote = ''

            item['id'] = id
            item['name'] = name
            item['movieInfo'] = movieinfo
            item['star'] = star
            item['quote'] = quote
            yield item
        nextlink = selector.xpath('//span[@class="next"]/link/@href').extract()
        if nextlink:
            nextlink = nextlink[0]
            print nextlink
            yield Request(self.url + nextlink, callback=self.parse)

