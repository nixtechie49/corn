# encoding:utf-8

__author__ = 'rock'
import re
import logging
import json

import tornado.web
from redis import ConnectionError, TimeoutError

from cn.rock import constants, collection, parsermap


class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('welcome.html')


class CollectionHandler(tornado.web.RequestHandler):
    def get(self):
        result = {}
        target = self.get_argument('target', None)
        db = self.get_argument('db', None)
        result['success'] = False
        result['msg'] = u'服务出错'
        if len(constants.REDIS_CONFIG) < 1:
            logging.debug('collection number ' + str(len(constants.REDIS_CONFIG)))
            result['msg'] = u'当前没有连接可用，请新建连接'
        else:
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

    def post(self):
        result = {}
        args = json.loads(self.request.body)
        logging.debug('new redis args : ' + str(args))
        print(args['redis']['ip'])
        result['success'] = True
        self.finish(result)


class KeyHandler(tornado.web.RequestHandler):
    def get(self):
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
            result['msg'] = u'连接Redis服务失败'
            logging.error(result['msg'] + e.message)
        except TimeoutError, e:
            result['success'] = False
            result['msg'] = u'连接Redis服务超时'
            logging.error(result['msg'] + e.message)
        # print(r.execute_command('keys', '*'))
        # data = json.dumps(keys, ensure_ascii=False)
        result['keys'] = keys
        logging.debug('response data is : ' + str(result))
        try:
            self.finish(result)
        except UnicodeDecodeError, e:
            logging.error('redis键转码失败:' + e.message)


class ValueHandler(tornado.web.RequestHandler):
    def get(self):
        key = self.get_argument('key')
        target = self.get_argument('col')
        db = self.get_argument('db')
        result = {}
        t = u'string'
        v = u''
        try:
            if target and key:
                r = collection.get_redis(target, db)
                t, v = collection.get_type_and_value(key, r)
            for (regex, p) in parsermap.MAP.items():
                if re.match(regex, key):
                    v = p.parse(v)
            result['success'] = True
        except Exception, e:
            msg = u'获取键值失败' + e.message
            logging.error(msg)
            result['success'] = False
            result['msg'] = msg
        result['key'] = key
        result['type'] = t
        result['value'] = v
        logging.debug('key:' + key + ' type:' + t + ' value:' + str(v))
        self.finish(result)

    def delete(self):
        result = {}
        key = self.get_argument('key')
        target = self.get_argument('col')
        db = self.get_argument('db')
        result['type'] = u'string'
        try:
            if target and key:
                r = collection.get_redis(target, db)
                res = collection.delete(r, key)
            result['success'] = res
            if not res:
                result['msg'] = u'删除失败'
        except Exception, e:
            msg = u'删除失败:' + e.message;
            logging.error(msg)
            result['success'] = False
            result['msg'] = msg
        self.finish(result)


class CommandHandler(tornado.web.RequestHandler):
    def post(self):
        result = {}
        args = json.loads(self.request.body)
        command = args['command']
        target = args['col']
        db = args['db']
        logging.debug('execute : ' + str(command))
        try:
            if target and command:
                r = collection.get_redis(target, db)
                res = collection.execute_command(r, command)
                logging.debug('execute command result : ' + str(res))
            result['success'] = res
        except Exception, e:
            msg = u'命令执行失败:' + e.message
            logging.error(msg)
            result['success'] = False
            result['msg'] = msg
        self.finish(result)