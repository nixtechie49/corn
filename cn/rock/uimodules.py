# encoding:utf-8
__author__ = 'rock'
from tornado.web import UIModule


class Collection(UIModule):
    def render(self, names, target, db=0, show_comments=False):
        return self.render_string("collection.html", names=names, target=target, db=db, show_comments=show_comments)


class Keys(UIModule):
    def render(self, target, db):
        return self.render_string("keys.html", target=target, db=db)


class Value(UIModule):
    def render(self):
        return self.render_string("value.html")