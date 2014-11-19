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
        target = self.get_argument('target', None)
        db = self.get_argument('db', None)
        result = {}
        collections = list(constants.REDIS_CONFIG.keys())
        dbs = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15')
        if not target:
            target = collections[0]
        if not db:
            db = constants.REDIS_CONFIG[target]['db']
        result['collections'] = collections
        result['dbs'] = dbs
        result['currentCol'] = target
        result['currentDB'] = db
        logging.debug('response data is : ' + str(result))
        self.write(result)


class KeyHandler(tornado.web.RequestHandler):
    def get(self):
        self.post()

    def post(self):
        target = self.get_argument('target', None)
        logging.debug('target is ' + target)
        db = self.get_argument('db', None)
        logging.debug('db is ' + db)
        r = collection.get_redis(target, db)
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
        result = {}
        t = 'string'
        v = ''
        if name and key:
            r = collection.get_redis(name, db)
            t, v = collection.get_type_and_value(key, r)
        for (regex, p) in parsermap.MAP.items():
            if re.match(regex, key):
                v = p.parse(v)
        result['type'] = t
        result['value'] = v
        self.write(result)
