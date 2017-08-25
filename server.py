# encoding:utf-8

import logging

import tornado.web

import kit
import routers
import settings
import sql
import worker

__author__ = 'rock'

application = tornado.web.Application(**settings.s)

application.add_handlers(r".*", routers.r)

if __name__ == "__main__":
    logging.basicConfig(format=kit.LOG_FORMAT, datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)
    application.listen(settings.PORT)
    instance = tornado.ioloop.IOLoop.instance()
    sql.init()
    worker.start()
    try:
        instance.start()
    except KeyboardInterrupt:
        instance.stop()
    worker.stop()
