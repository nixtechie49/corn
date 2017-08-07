# encoding:utf-8

import logging

import tornado.web

import kit
import routers
import settings
import sql

__author__ = 'rock'

application = tornado.web.Application(**settings.s)

application.add_handlers(r".*", routers.r)

if __name__ == "__main__":
    logging.basicConfig(format=kit.LOG_FORMAT, datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)
    sql.init()
    application.listen(settings.PORT)
    tornado.ioloop.IOLoop.instance().start()
