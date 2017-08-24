# encoding:utf-8

from kazoo.client import KazooClient

__author__ = 'rock'

__client__ = {}


class Client:
    def __init__(self, hosts, **kwargs):
        if hosts not in __client__:
            c = KazooClient(hosts=hosts, **kwargs)
            c.start()
            self.conn = __client__[hosts] = c

    def get(self, path):
        return self.conn.get(path)

    def get_watch(self, path, func):
        return self.conn.get(path=path, watch=func)

    def watch(self, path, func):
        return self.conn.exists(path=path, watch=func)

    def stop(self):
        return self.conn.stop()


def shutdown():
    for c in __client__:
        __client__[c].stop()
