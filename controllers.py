# encoding:utf-8

import tornado

__author__ = 'rock'


class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        print('111')
        self.render('hello.html')
