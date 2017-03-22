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
        'DOWNLOAD_DELAY': 5
    }

    def start_requests(self):
        for query in [u'cubbeli+ahmet+hoca']:
            url = 'https://www.youtube.com/results?q=' + query

            yield Request(url)

    def parse(self, response):

        public_html = PyQuery(response.body)

        selectors = public_html('.item-section .yt-lockup-dismissable')

        for k in range(len(selectors)):

            selector = selectors.eq(k)
            item = {}

            # Unicode problem
            # http://stackoverflow.com/questions/1177316/decoding-double-encoded-utf8-in-python

            title = selector('.yt-lockup-title a').text()
            title = title.encode('raw_unicode_escape').decode('utf-8')
            item['title'] = title

            content = selector('.yt-lockup-description').text()
            content = content.encode('raw_unicode_escape').decode('utf-8')
            item['content'] = content

            url = selector('.yt-lockup-title a').attr('href')

            item['url'] = 'https://www.youtube.com/embed/' + url.split('v=')[-1]

            picture = selector('.yt-thumb-simple img').attr('data-thumb')

            if picture is None:
                picture = selector('.yt-thumb-simple img').attr('src')

            item['picture'] = picture.split('?')[0]
            item['category'] = ''
            item['country'] = 'TR'

            duration_text = selector('.accessible-description').text()
            duration_text = duration_text.split(':')

            duration = -1
            if len(duration_text) == 3:
                duration = int(duration_text[1].strip())*60 + \
                           int(duration_text[2].rstrip('.'))
            elif len(duration_text) == 4:
                duration = int(duration_text[1].strip())*3600 + \
                           int(duration_text[2].strip())*60 + \
                           int(duration_text[3].rstrip('.'))

            item['duration'] = duration


            yield item


