from pyquery import PyQuery
from scrapy.http import Request
import scrapy
import datetime
from utilities.date_converter import DateConverter
import urllib
import re


class YoutubeComSpider(scrapy.Spider):

    name = 'youtube.com.spider'

    custom_settings = {
        'ITEM_PIPELINES': {
            # 'web_crawler.spiders.video_pipeline.VideoPipeline': 1,
        },
        'DOWNLOAD_TIMEOUT': 60,
    }

    def start_requests(self):
        for query in ['mehmet']:
            url = 'https://www.youtube.com/results?q=' + query

            yield Request(url)

    def parse(self, response):

        public_html = PyQuery(response.body)

        selectors = public_html('.item-section .yt-lockup')

        for selector in selectors:
            item = {}
            title = selector
            content = ''
            news_publish_date = ''

            yield item


