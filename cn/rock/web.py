# encoding:utf-8
__author__ = 'rock'
import re
import logging
import json

import tornado.web

from cn.rock import constants, collection, parsermap


class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        self.post()

    def post(self):
        if len(constants.REDIS_CONFIG) < 1:
            raise tornado.web.HTTPError(403)
        self.render('welcome.html')


class CollectionHandler(tornado.web.RequestHandler):
    def get(self):
        self.post()

    def post(self):
        data = list(constants.REDIS_CONFIG.keys())
        logging.debug('response data is : ' + str(data))
        self.write(data)


class KeyHandler(tornado.web.RequestHandler):
    def get(self):
        self.post()

    def post(self):
        target = self.get_argument('target', None)
        db = self.get_argument('db', None)
        r = collection.getRedis(target, db)
        keys = r.keys()
        data = json.dumps(keys, ensure_ascii=False)
        logging.debug('response data is : ' + str(data))
        self.write(data)


class ValueHandler(tornado.web.RequestHandler):
    def get(self):
        self.post()

    def post(self):
        key = self.get_argument('key')
        name = self.get_argument('col')
        db = self.get_argument('db')
        value = ''
        if name and key:
            r = collection.getRedis(name, db)
            value = str(collection.getValue(key, r))
        for (regex, h) in parsermap.MAP.items():
            print(regex, h)
            if re.match(regex, key):
                value = h.do(value)
        self.write(value)
