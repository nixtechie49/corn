# encoding:utf-8
__author__ = 'rock'

import tornado.ioloop
import tornado.web

from cn.rock import controller
from cn.rock import constants


PORT = 7878
settings = {'debug': True,
            'static_path': constants.STATIC_DIR_PATH,
            'template_path': constants.TEMPLATE_DIR_PATH,
}

application = tornado.web.Application([
                                          (r"/", controller.HomeHandler),
                                          (r"/collection/", controller.CollectionHandler),
                                          (r"/key/", controller.KeyHandler),
                                          (r"/value/", controller.ValueHandler),
                                          (r"/command/", controller.CommandHandler),
                                      ], **settings)

from cn.rock import collection
import logging

if __name__ == "__main__":
    logging.basicConfig(format=constants.LOG_FORMAT, datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)
    collection.load_collection_config()
    application.listen(PORT)
    tornado.ioloop.IOLoop.instance().start()
