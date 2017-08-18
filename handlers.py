# encoding:utf-8

import json
import logging

from tornado.web import RequestHandler

import kit
import sql
from connection import Redis
from models import ConnInfo

__author__ = 'rock'


class HomeHandler(RequestHandler):
    def get(self):
        self.render('hello.html')


class KeyHandler(RequestHandler):
    def get(self, conn_id):
        conn = sql.get(ConnInfo, conn_id)
        if kit.log_level(logging.DEBUG):
            logging.debug('get conn:%s', conn)
        settings = {'url': 'redis://172.25.45.241:5568/0'}
        r = Redis(**settings)
        keys = r.scan()
        if kit.log_level(logging.DEBUG):
            logging.debug('load keys:%s', keys)
        self.write(kit.get_success(keys))


class ValueHandler(RequestHandler):
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
        self.write(kit.get_success(j))


class ConnectionHandler(RequestHandler):
    def post(self, *args, **kwargs):
        if kit.log_level(logging.DEBUG):
            logging.debug('args: %s', self.request.body)
        conn = json.loads(str(self.request.body, encoding='utf-8'))
        sql.add_connection(conn)
        self.write(kit.get_success())

    def get(self):
        data = sql.query(ConnInfo)
        self.write(kit.get_success(data))


class ConnHandler(RequestHandler):
    def get(self, conn_id):
        self.write(kit.get_success())
