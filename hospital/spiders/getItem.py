#coding: utf-8

import re
import random
import logging
import redis
import scrapy
import requests
from scrapy.http import Request
from scrapy.utils.log import configure_logging
from hospital.items import HospitalItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from requests.exceptions import ConnectTimeout, ReadTimeout

configure_logging(install_root_handler=False)
#定义了logging的些属性
logging.basicConfig(
    filename='scrapy.log',
    format='%(levelname)s: %(levelname)s: %(message)s',
    level=logging.INFO
)
#运行时追加模式
logger = logging.getLogger('SimilarFace')

pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
redisClient = redis.StrictRedis(connection_pool=pool)

def getIp():
    times = 0
    while True:
        if times > 3:
            return None,"" 
        count = redisClient.llen("PROXY_IPS")
        index = random.randint(0, count)
        proxyIp = redisClient.lindex("PROXY_IPS", index)
        proxies = {'http': 'http://{0}'.format(proxyIp)}
        try:
            reqUrl = "http://www.poi86.com/poi/1008130.html"
            r = requests.get(reqUrl, proxies=proxies, timeout=3)
            if r.status_code == 200:
                return proxies['http'], r.text
        except ConnectTimeout:
            logger.info("[[connect timeout wait for 3s to try again]]" + proxies['http'])
        except ReadTimeout:
            times += 1
            logger.info("[[read timeout {0} times]]".format(times))
        except Exception as e:
            logger.info("[[proxy error wait for 3s to try again]]" + proxies['http']+" "+str(e.message))
            #redisClient.lrem("PROXY_IPS", 0, proxyIp)

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
            proxy, content = getIp()
            yield Request(url=url, meta={"proxy":proxy}, callback=self.parseItem)

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
