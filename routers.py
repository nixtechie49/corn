# encoding:utf-8

import handlers

__author__ = 'rock'

r = [
    (r"/", handlers.HomeHandler),
    (r"/key", handlers.KeyHandler),
]
