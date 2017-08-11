# encoding:utf-8

import json
import logging

import tornado

import kit
from connection import Redis

__author__ = 'rock'


class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('hello.html')


class KeyHandler(tornado.web.RequestHandler):
    def get(self):
        settings = {'url': 'redis://172.25.45.241:5568/0'}
        r = Redis(**settings)
        j = json.dumps(r.scan(), default=kit.date_handler)
        if kit.log_level(logging.DEBUG):
            logging.debug('load keys:%s', j)
        self.write(j)


class ValueHandler(tornado.web.RequestHandler):
    def get(self, key):
        if kit.log_level(logging.DEBUG):
            logging.debug('load value by key: %s', key)
        # settings = {'url': 'redis://172.24.7.30:6379/0'}
        settings = {'url': 'redis://172.25.45.240:5590/0'}
        r = Redis(**settings)
        v = r.get(key)
        if v:
            j = str(v, encoding='utf-8')
        else:
            j = 'nil'
        if kit.log_level(logging.DEBUG):
            logging.debug('load value (%s):%s', key, j)
        self.write(j)