#coding: utf-8

import re
import logging
import redis
import scrapy
import requests
from scrapy.http import Request
from scrapy.utils.log import configure_logging
from hospital.items import HospitalItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

configure_logging(install_root_handler=False)
#定义了logging的些属性
logging.basicConfig(
    filename='scrapy.log',
    format='%(levelname)s: %(levelname)s: %(message)s',
    level=logging.INFO
)
#运行时追加模式
logger = logging.getLogger('SimilarFace')

class HospitalSpider(CrawlSpider):
    name = "hospital"
    start_urls = ["http://www.poi86.com/poi/tag/209/1.html"]

    rules = (
        #"http://www.poi86.com"+x
        Rule(LinkExtractor(restrict_xpaths = ("//ul[@class='pagination']/li"),process_value=lambda x: x),\
                callback = "getRecord", follow=True),
    )

    def getRecord(self, response):
        urls = response.xpath("//tr/td/a[not(contains(@href,'district') or contains(@href,'category'))]/@href").extract()
        for url in urls:
            url = "http://www.poi86.com" + url
            yield Request(url=url, callback=self.parseItem)

    def parseItem(self, response):
        item = HospitalItem()
        item["name"] = response.xpath('//h1/text()').extract_first() 

        res = response.xpath("//ul/li[@class='list-group-item']/a/text()").extract()
        item["province"] = res[0]
        item["city"] = res[1]
        item["district"] = res[2]
        item["label"] = res[3].replace("(","")

        res = response.xpath("//ul/li[@class='list-group-item']").extract()
        item["address"] = re.findall("</span>(.*)</li>",res[3])[0]
        item["phone"] = re.findall("</span>(.*)</li>",res[4])[0]
        item["category"] = ""
        item["groundpos"] = re.findall("</span>(.*)</li>",res[-3])[0]
        item["marspos"] = re.findall("</span>(.*)</li>",res[-2])[0]
        item["baidupos"] = re.findall("</span>(.*)</li>",res[-1])[0]

        yield item
