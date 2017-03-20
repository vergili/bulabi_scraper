from pyquery import PyQuery
from scrapy.http import Request
import scrapy
from scrapy.conf import settings
import datetime
from utilities.date_converter import DateConverter
import urllib
import re


class YoutubeComSpider(scrapy.Spider):

    name = 'youtube.com.spider'

    custom_settings = {
        'ITEM_PIPELINES': {
            'web_crawler.spiders.video_pipeline.VideoPipeline': 1,
        },
        'DOWNLOAD_TIMEOUT': 60,
    }

    def start_requests(self):
        for query in ['mehmet']:
            url = 'https://www.youtube.com/results?q=' + query

            yield Request(url)

    def parse(self, response):

        public_html = PyQuery(response.body)

        selectors = public_html('.item-section .yt-lockup-dismissable')

        for k in range(len(selectors)):

            selector = selectors.eq(k)
            item = {}

            title = selector('.yt-lockup-title').text()

            title = title.encode('UTF-8')

            print title

            item['title'] = selector('.yt-lockup-title').text().encode('UTF-8')

            print item['title']

            item['content'] = selector('.yt-lockup-description').text()

            url = selector('.yt-lockup-title a').attr('href')

            item['url'] = 'https://www.youtube.com/embed/' + url.split('v=')[-1]

            picture = selector('.yt-thumb-simple img').attr('src')
            item['picture'] = picture.split('?')[0]
            item['category'] = ''
            item['country'] = 'TR'

            yield item


