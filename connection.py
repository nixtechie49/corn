# encoding:utf-8

import logging
import os
import sqlite3

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


class SqlLite:
    def __init__(self, db_name):
        if not os.path.exists(db_name):
            self.conn = sqlite3.connect(db_name)
            self.__create_table()
        else:
            self.conn = sqlite3.connect(db_name)

    def __create_table(self):
        table_conn = "CREATE TABLE `REDIS_CONN` " \
                     "(`ID` INTEGER PRIMARY KEY AUTOINCREMENT," \
                     "`URL` varchar(256) UNIQUE NOT NULL," \
                     "`HOST` varchar(256) NOT NULL," \
                     "`PORT` int(11) NOT NULL," \
                     "`DB` tinyint(4) NOT NULL)"
        cs = self.conn.cursor()
        cs.execute(table_conn)
        self.conn.commit()
        logging.debug('create table on conn:[%s]', self.conn)

    def add_conn(self, redis_info):
        logging.debug('add redis info %s', redis_info)
        add_conn = "INSERT INTO `REDIS_CONN` (`URL`,`HOST`,`PORT`,`DB`) VALUES " \
                   "('{url}' ,'{host}' ,{port} ,{db})".format(url=redis_info['url'], host=redis_info['host'],
                                                              port=redis_info['port'], db=redis_info['db'])
        logging.debug('add redis info sql [%s]', add_conn)
        cs = self.conn.cursor()
        cs.execute(add_conn)
        self.conn.commit()

    def get_conn(self, url):
        logging.debug('get redis info %s', url)
        get_conn = "SELECT * FROM `REDIS_CONN` WHERE URL = '{url}'".format(url=url)
        logging.debug('get redis info sql [%s]', get_conn)
        cs = self.conn.cursor()
        cs.execute(get_conn)
        result = cs.fetchone()
        if kit.log_level(logging.DEBUG):
            logging.debug('get redis info result %s', result)
        return result

    def get_conn_all(self):
        logging.debug('get redis info all')
        get_all = "SELECT * FROM `REDIS_CONN` ORDER BY ID DESC"
        cs = self.conn.cursor()
        cs.execute(get_all)
        result = cs.fetchall()
        if kit.log_level(logging.DEBUG):
            logging.debug('get redis info all result %s', result)
        return result
