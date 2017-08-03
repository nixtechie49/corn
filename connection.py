# encoding:utf-8

import logging
import os
import sqlite3

import redis

__author__ = 'rock'


class Redis:
    cp = {}

    def __init__(self, **settings):
        if 'url' not in settings:
            self.host = settings['host']
            self.port = settings['port']
            self.db = settings['db']
            url = Redis.url(self.host, self.port, self.db)
        else:
            url = settings['url']
        logging.debug('connect url = %s', url)
        if url not in Redis.cp:
            conn = redis.ConnectionPool.from_url(url)
            Redis.cp[url] = conn
        else:
            conn = Redis.cp[url]
        logging.debug('try connect redis(%s)', conn.connection_kwargs)
        self.conn = redis.StrictRedis(connection_pool=conn)
        if self.test():
            logging.info('connect redis(%s) success', conn.connection_kwargs)

    def test(self):
        good = self.conn.ping()
        logging.debug('redis connection is good[%s]', good)
        return good

    def db_size(self):
        return self.conn.dbsize()

    @staticmethod
    def url(host, port, db):
        return r'redis://' + host + r':' + str(port) + r'/' + str(db)


class SqlLite:
    def __init__(self, db_name):
        if not os.path.exists(db_name):
            self.conn = sqlite3.connect(db_name)
            self.__create_table()
        else:
            self.conn = sqlite3.connect(db_name)

    def __create_table(self):
        table_conn = r"CREATE TABLE `REDIS_CONN` " \
                     r"(`ID` INTEGER PRIMARY KEY AUTOINCREMENT," \
                     r"`URL` varchar(256) NOT NULL," \
                     r"`HOST` varchar(256) NOT NULL," \
                     r"`PORT` int(11) NOT NULL," \
                     r"`DB` tinyint(4) NOT NULL)"
        cs = self.conn.cursor()
        cs.execute(table_conn)
        self.conn.commit()
        logging.debug('create table on conn:[%s]', self.conn)
