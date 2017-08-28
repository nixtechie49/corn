# encoding:utf-8

import logging
from logging import config

import tornado.web

import routers
import settings
import sql
import worker

__author__ = 'rock'

application = tornado.web.Application(**settings.s)

application.add_handlers(r".*", routers.r)

if __name__ == "__main__":
    logging.config.fileConfig('./log.conf')
    application.listen(settings.PORT)
    instance = tornado.ioloop.IOLoop.instance()
    sql.init()
    worker.start()
    try:
        instance.start()
    except KeyboardInterrupt:
        instance.stop()
    worker.stop()
