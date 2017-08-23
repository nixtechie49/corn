# encoding:utf-8

import handlers

__author__ = 'rock'

r = [
    (r"/", handlers.HomeHandler),
    (r"/(?P<conn_id>[\d]+)/key", handlers.KeyHandler),
    (r"/connection", handlers.ConnectionHandler),
    (r"/connection/(^([1-9][0-9]*)$)", handlers.ConnHandler),
    (r"/(?P<conn_id>[\d]+)/value/(?P<key>[\S]+)", handlers.ValueHandler),
]
