# coding: utf-8
from __future__ import absolute_import
import os
import sys
from scrapy.conf import settings
from .base import Base, BaseValidator
try:
    import dev_appserver
    dev_appserver.fix_sys_path()
    from google.appengine.ext import ndb
except ImportError:
    print('Please make sure the App Engine SDK is in your PYTHONPATH.')
    raise


class Video(Base):
    title = ndb.TextProperty(default='')
    content = ndb.TextProperty(default='')
    duration = ndb.IntegerProperty()

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
    def insert_video(title, content, url, picture, category, country, duration):

        video = Video.get_by('url', url)
        if video is None:
            # user_db.auth_ids.append(auth_id)

            video = Video(
                title=title,
                content=content,
                url=url,
                picture=picture,
                category=category,
                country=country,
                duration = duration
            )

            video.put()
            return video

