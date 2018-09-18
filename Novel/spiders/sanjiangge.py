# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.loader import ItemLoader
from urllib.parse import urljoin

from Novel.items import NovelMysqlItem


class SanjianggeSpider(scrapy.Spider):
    name = 'sanjiangge'
    allowed_domains = ['www.shushu8.com']
    start_urls = ['http://www.shushu8.com/yingxiongzhi/']

    def parse(self, response):
        nodes=response.css('div.dirconone ul li a')
        for node in nodes:
            nove_url=node.css('::attr(href)').extract_first()
            nove_title=node.css('::text').extract_first()
            Request(urljoin(response.url,nove_url),meta={'title',nove_title},callback=self.parse_detail)
        pass
    def parse_detail(self,response):
        itemLoader=ItemLoader(item=NovelMysqlItem(),response=response)
        itemLoader.add_css("title",response.meta.get("title"))
        itemLoader.add_css("content",response.css('div.page-content pre.note::text  ').extract_first())
