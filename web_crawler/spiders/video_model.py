# coding: utf-8
from __future__ import absolute_import
import os
import sys
from scrapy.conf import settings
try:
    sys.path.append(settings['GOOGLE_APPENGINE_DIR'])
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = settings['GOOGLE_APPLICATION_CREDENTIALS']
    import dev_appserver
    dev_appserver.fix_sys_path()
    from google.appengine.ext import ndb
except ImportError:
    print('Please make sure the App Engine SDK is in your PYTHONPATH.')
    raise


class Video(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    modified = ndb.DateTimeProperty(auto_now=True)
    version = ndb.IntegerProperty(default=1489501303)
    title = ndb.TextProperty(default='')
    content = ndb.TextProperty(default='')

    url = ndb.StringProperty(default='')
    picture = ndb.StringProperty(default='')
    category = ndb.StringProperty(default='')
    country = ndb.StringProperty(default='')

    PUBLIC_PROPERTIES = ['key', 'version', 'created', 'modified', 'title',
                         'content', 'url', 'picture', 'category', 'country']


    @classmethod
    def get_by_user(cls, user):
        return cls.query().filter(cls.user_id == user.user_id()).get()

    @classmethod
    def get_by_key(cls, key):
        key = ndb.Key(urlsafe=key)
        video_db = key.get()
        return video_db

    @staticmethod
    def insert_video(title, content, url, picture, category, country):

        video_db = Video(
            title=title,
            content=content,
            url=url,
            picture=picture,
            category=category,
            country=country
        )
        video_db.put()
        return video_db
