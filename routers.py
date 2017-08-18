# encoding:utf-8

import handlers

__author__ = 'rock'

r = [
    (r"/", handlers.HomeHandler),
    (r"/(^([1-9][0-9]*))/key$", handlers.KeyHandler),
    (r"/connection", handlers.ConnectionHandler),
    (r"/connection/(^([1-9][0-9]*)$)", handlers.ConnHandler),
    (r"/value/([\s\S]*)", handlers.ValueHandler),
]
