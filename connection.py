# encoding:utf-8

import logging

import redis

import kit

__author__ = 'rock'


class Redis:
    cp = {}

    def __init__(self, **settings):
        if 'url' not in settings:
            url = Redis.url(settings['host'], settings['port'], settings['db'])
        else:
            url = settings['url']
        self.url = url
        logging.debug('connect url = %s', url)
        if url not in Redis.cp:
            conn = redis.ConnectionPool.from_url(url, max_connections=128)
            Redis.cp[url] = conn
        else:
            conn = Redis.cp[url]
        logging.debug('try connect redis(%s)', conn.connection_kwargs)
        self.conn = redis.StrictRedis(connection_pool=conn)
        if self.test():
            logging.info('connect redis(%s) success', conn.connection_kwargs)
            self.host = conn.connection_kwargs.get('host')
            self.port = conn.connection_kwargs.get('port')
            self.db = conn.connection_kwargs.get('db')

    def test(self):
        logging.debug('test connect redis(%s)', self.conn)
        good = self.conn.ping()
        logging.debug('redis connection is good[%s]', good)
        return good

    def db_size(self):
        return self.conn.dbsize()

    def scan(self, match='*', index=0):
        result = self.conn.scan(cursor=index, match=match, count=100)
        size = len(result[1])
        if kit.log_level(logging.DEBUG):
            logging.debug('scan %s from %d result(%d) : %s', match, index, size, result)
        if result[0] != 0 and size == 0:
            return self.scan(match, index)
        return result

    @staticmethod
    def url(host, port, db):
        return r'redis://' + host + r':' + str(port) + r'/' + str(db)
