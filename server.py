# encoding:utf-8

import logging
import os

import tornado.web

import handlers

__author__ = 'rock'
ROOT_PATH = os.path.join(os.path.dirname(__file__), './')

CONFIG_DIR_PATH = os.path.join(ROOT_PATH, 'config/')
TEMPLATE_DIR_PATH = os.path.join(ROOT_PATH, 'templates/')
STATIC_DIR_PATH = os.path.join(ROOT_PATH, 'static/')

PORT = 8001
DOMAIN = r'http://redis.explorer.local'

settings = {'debug': True,
            'static_path': STATIC_DIR_PATH,
            'template_path': TEMPLATE_DIR_PATH,
            }

application = tornado.web.Application(**settings)

application.add_handlers(r".*", [
    (r"/", handlers.HomeHandler),
])

LOG_FORMAT = "[%(asctime)s]-[%(levelname)s] : %(message)s [from %(module)s.%(funcName)s.%(lineno)d]"

if __name__ == "__main__":
    logging.basicConfig(format=LOG_FORMAT, datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)
    application.listen(PORT)
    tornado.ioloop.IOLoop.instance().start()
