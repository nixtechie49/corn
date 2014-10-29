# encoding:utf-8
__author__ = 'rock'
import tornado.ioloop
import tornado.web

from cn.rock import web
from cn.rock import constants
from cn.rock import uimodules


PORT = 7878
settings = {'debug': True,
            'static_path': constants.STATIC_DIR_PATH,
            'template_path': constants.TEMPLATE_DIR_PATH,
            'ui_modules': uimodules,
}

application = tornado.web.Application([
                                          (r"/", web.HomeHandler),
                                          (r"/value/", web.ValueHandler),
                                      ], **settings)

from cn.rock import collection

if __name__ == "__main__":
    collection.loadConllectionsConfig()
    application.listen(PORT)
    tornado.ioloop.IOLoop.instance().start()
