# -*- coding: utf-8 -*-
import scrapy
from qc.items import QcItem


class A51Spider(scrapy.Spider):
    name = 'a51'
    # allowed_domains = ['51job.com']
    start_urls = ['https://search.51job.com/list/010000,000000,0000,00,9,99,python,2,1.html']

    def parse(self, response):
        print(response.body)
        node_list = response.xpath('//div[@class="el"]')

        for node in node_list:
            item = QcItem()
            item['work_name'] = node.xpath('./p/span/a/@title')
            item['company'] = node.xpath('./span/a/title')

            item['work_position'] = node.xpath('./span[class="t3"]/text()')
            item['salary'] = node.xpath('./span[class="t4"]/text()')

            item['publishTime'] = node.xpath('./span[class="t5"]/text()')
            item['content'] = node.xpath('./p/span/a/@title')
            item['contact'] = node.xpath('./p/span/a/@title')


            detail_href = node.xpath('./p/span/a/@href').extract_first()
            if detail_href is None:
                continue
            yield scrapy.Request(url=detail_href,callback=self.detail,meta={'item':item})

    def detail(self,response):
        item = response['item']
        content1 = response.xpath['']
        content2 = response.xpath['']
        yield item