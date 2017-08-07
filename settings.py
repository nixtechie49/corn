# encoding:utf-8

import kit

__author__ = 'rock'

PORT = 8001
DOMAIN = r'http://redis.explorer.local'
DEBUG = True

s = {'debug': DEBUG,
     'static_path': kit.STATIC_DIR_PATH,
     'template_path': kit.TEMPLATE_DIR_PATH,
     }
