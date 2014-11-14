# encoding:utf-8
__author__ = 'rock'
import re

import tornado.web

from cn.rock import constants, collection, parsermap


class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        self.post()

    def post(self):
        if len(constants.REDIS_CONFIG) < 1:
            raise tornado.web.HTTPError(403)
        target = self.get_argument('target', None)
        db = self.get_argument('db', None)
        names = list(constants.REDIS_CONFIG.keys())
        if names and not target:
            target = names[-1]
        if not db:
            db = constants.REDIS_CONFIG[target]['db']
        self.render('welcome.html', names=names, target=target, db=db)


import json


class CollectionHandler(tornado.web.RequestHandler):
    def get(self):
        result = {}
        target = self.get_argument('target', None)
        db = self.get_argument('db', None)
        names = list(constants.REDIS_CONFIG.keys())
        if names and not target:
            target = names[0]
        if not db:
            db = constants.REDIS_CONFIG[target]['db']
        result['db'] = str(db)
        r = collection.getRedis(target, db)
        keys = r.keys()
        result['keys'] = keys
        data = json.dumps(result, ensure_ascii=False)
        self.write(data)


class ValueHandler(tornado.web.RequestHandler):
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
