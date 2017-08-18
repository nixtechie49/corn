# encoding:utf-8

import handlers

__author__ = 'rock'

r = [
    (r"/", handlers.HomeHandler),
    (r"/connection", handlers.ConnectionHandler),
    (r"/connection/(^([1-9][0-9]*)$)", handlers.ConnHandler),
    (r"/key", handlers.KeyHandler),
    (r"/value/([\s\S]*)", handlers.ValueHandler),
]
