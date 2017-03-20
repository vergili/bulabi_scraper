import os
import sys
from scrapy import signals
from scrapy.conf import settings
from scrapy.xlib.pydispatch import dispatcher
try:
    from google.appengine.ext import ndb
    from google.appengine.ext.remote_api import remote_api_stub
except ImportError:
    print('Please make sure the App Engine SDK is in your PYTHONPATH.')
    raise


class VideoPipeline(object):

    def __init__(self):
        dispatcher.connect(self.spider_closed, signal=signals.spider_closed)

    def spider_closed(self, spider):
        return

    def process_item(self, item, spider):

        from video_model import Video

        remote_api_stub.ConfigureRemoteApiForOAuth(
            '{}.appspot.com'.format(settings['GOOGLE_APPID']), '/_ah/remote_api')

        # Video().insert_video(title=title,content=content,picture=picture, category=category, url=url, country=country)

        Video().insert_video(**item)

        return item
