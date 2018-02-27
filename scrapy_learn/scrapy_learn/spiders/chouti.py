# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector, HtmlXPathSelector
from scrapy.http import Request
from scrapy.http.cookies import CookieJar

class ChoutiSpider(scrapy.Spider):
    name = 'chouti'
    # allowed_domains = ['chouti.com/']
    start_urls = ['http://dig.chouti.com/']
    cookie_dict = None

    def parse(self, response):
        cookie_obj = CookieJar()
        cookie_obj.extract_cookies(response, response.request)
        self.cookie_dict = cookie_obj._cookies
        # 真正cookie cookie_obj._cookies

        yield Request(
            url='http://dig.chouti.com/login',
            method='POST',
            headers={'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'},
            body="phone=8618565802242&password=q8620303&oneMonth=1",
            cookies=self.cookie_dict,
            callback=self.check_login
        )

    def check_login(self, response):
        yield Request(url='http://dig.chouti.com/', callback=self.like)

    def like(self, response):
        id_list = Selector(response=response).xpath('//div[@share-linkid]/@share-linkid').extract()
        for nid in id_list:
            url = 'http://dig.chouti.com/link/vote?linksId=%s'%(nid)
            yield Request(
                url=url,
                method='POST',
                cookies=self.cookie_dict,
                callback=self.show
            )

        page_urls = Selector(response).xpath('//div[@id="dig_lcpage"]//a/@href').extract()
        for page in page_urls:
            url = 'http://dig.chouti.com%s' % page
            yield Request(url=url, callback=self.like)

    def show(self, response):
        print(response.text)


