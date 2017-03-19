import random
from scrapy.conf import settings
# from scrapy.http import HtmlResponse
# from scrapy.utils.python import to_bytes
# from selenium import webdriver
# from scrapy import signals


class RandomUserAgentMiddleware(object):

    def process_request(self, request, spider):
        ua = random.choice(settings.get('USER_AGENT_LIST'))
        if ua:
            request.headers.setdefault('User-Agent', ua)


class ProxyMiddleware(object):

    def process_request(self, request, spider):
        request.meta['proxy'] = settings.get('HTTP_PROXY')

#
# class SeleniumMiddleware(object):
#     """
#     http://stackoverflow.com/questions/31174330/passing-selenium-response-url-to-scrapy/31186730#31186730
#     """
#     def process_request(self, request, spider):
#         driver = webdriver.Firefox()
#         driver.get(request.url)
#
#         body = driver.page_source
#         return HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=request)
#
#
# class SeleniumMiddleware2(object):
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         middleware = cls()
#         crawler.signals.connect(middleware.spider_opened, signals.spider_opened)
#         crawler.signals.connect(middleware.spider_closed, signals.spider_closed)
#         return middleware
#
#     def process_request(self, request, spider):
#         request.meta['driver'] = self.driver  # to access driver from response
#         self.driver.get(request.url)
#         body = to_bytes(self.driver.page_source)  # body must be of type bytes
#         return HtmlResponse(self.driver.current_url, body=body, encoding='utf-8', request=request)
#
#     def spider_opened(self, spider):
#         self.driver = webdriver.Firefox()
#
#     def spider_closed(self, spider):
#         self.driver.close()
