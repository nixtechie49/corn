# encoding:utf-8

import tornado
import logging
from connection import Redis,SqlLite

__author__ = 'rock'


class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        settings = {'url': 'redis://172.24.7.30:6379/0'}
        r = Redis(**settings)
        logging.debug(SqlLite(r'data.db'))
        self.render('hello.html')
