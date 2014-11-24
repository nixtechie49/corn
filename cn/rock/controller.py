# encoding:utf-8
from redis import ConnectionError, TimeoutError

__author__ = 'rock'
import re
import logging

import tornado.web

from cn.rock import constants, collection, parsermap


class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        self.post()

    def post(self):
        if len(constants.REDIS_CONFIG) < 1:
            logging.debug('collection number ' + str(len(constants.REDIS_CONFIG)))
            self.redirect('/input/')
        else:
            self.render('welcome.html')


class CollectionHandler(tornado.web.RequestHandler):
    def get(self):
        self.post()

    def post(self):
        result = {}
        target = self.get_argument('target', None)
        db = self.get_argument('db', None)
        result['success'] = False
        result['msg'] = '服务出错'
        collections = list(constants.REDIS_CONFIG.keys())
        if not target:
            target = collections[0]
        if not db:
            db = constants.REDIS_CONFIG[target]['db']
        result['collections'] = collections
        result['dbs'] = constants.DBS
        result['currentCol'] = target
        result['currentDB'] = db
        logging.debug('response data is : ' + str(result))
        result['success'] = True
        self.finish(result)


class KeyHandler(tornado.web.RequestHandler):
    def get(self):
        self.post()

    def post(self):
        result = {}
        target = self.get_argument('target', None)
        logging.debug('target is ' + target)
        db = self.get_argument('db', None)
        logging.debug('db is ' + db)
        r = collection.get_redis(target, db)
        keys = []
        try:
            keys = r.keys()
            result['success'] = True
        except ConnectionError, e:
            result['success'] = False
            result['msg'] = u'redis connection error.'
            logging.error(result['msg'] + e.message)
        except TimeoutError, e:
            result['success'] = False
            result['msg'] = u'redis connection timeout.'
            logging.error(result['msg'] + e.message)
        # print(r.execute_command('keys', '*'))
        # data = json.dumps(keys, ensure_ascii=False)
        result['keys'] = keys
        logging.debug('response data is : ' + str(result))
        try:
            self.finish(result)
        except UnicodeDecodeError, e:
            logging.error('get redis key error:' + e.message)


class ValueHandler(tornado.web.RequestHandler):
    def get(self):
        self.post()

    def post(self):
        key = self.get_argument('key')
        name = self.get_argument('col')
        db = self.get_argument('db')
        result = {}
        t = u'string'
        v = ''
        try:
            if name and key:
                r = collection.get_redis(name, db)
                t, v = collection.get_type_and_value(key, r)
            for (regex, p) in parsermap.MAP.items():
                if re.match(regex, key):
                    v = p.parse(v)
            result['success'] = True
        except Exception, e:
            logging.error('get value error' + e.message)
            result['success'] = False
            result['msg'] = 'get value error'
        result['key'] = key
        result['type'] = t
        result['value'] = v
        logging.debug('key:' + key + ' type:' + t + ' value:' + str(v))
        self.finish(result)


class DeleteHandler(tornado.web.RequestHandler):
    def get(self):
        self.delete()

    def post(self):
        self.delete()

    def delete(self):
        result = {}
        key = self.get_argument('key')
        name = self.get_argument('col')
        db = self.get_argument('db')
        result['type'] = u'string'
        try:
            if name and key:
                r = collection.get_redis(name, db)
                res = collection.delete(r, key)
                logging.debug(res)
            result['success'] = res
        except Exception, e:
            logging.error('delete error' + e.message)
            result['success'] = False
            result['msg'] = 'delete error'
        self.finish(result)


class InputHandler(tornado.web.RequestHandler):
    def get(self):
        self.post()

    def post(self):
        self.render('input.html')