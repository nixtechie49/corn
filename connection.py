# encoding:utf-8

import logging

from redis import StrictRedis
from rediscluster import StrictRedisCluster
from rediscluster.connection import ClusterConnectionPool

import kit

__author__ = 'rock'


class Redis:
    def __init__(self, **settings):
        if 'url' not in settings:
            url = Redis.url(settings['host'], settings['port'], settings['db'])
        else:
            url = settings['url']
        logging.debug('connect url = %s', url)
        self.conn = StrictRedis.from_url(url=url)
        if self.test():
            logging.info('connect redis(%s) success', self.conn)

    def test(self):
        logging.debug('test connect redis(%s)', self.conn)
        good = self.conn.ping()
        logging.debug('redis connection is good[%s]', good)
        return good

    def db_size(self):
        return self.conn.dbsize()

    def scan(self, match='*', index=0):
        # result = self.conn.eval("return redis.call('scan','0','MATCH',KEYS[1],'COUNT',1000)", 1, '*')
        result = self.conn.scan(cursor=index, match=match, count=100)
        size = len(result[1])
        if kit.log_level(logging.DEBUG):
            logging.debug('scan %s from %d result(%d) : %s', match, index, size, result)
        if result[0] != 0 and size == 0:
            return self.scan(match, index)
        return result

    def get(self, key):
        logging.debug('get value by key: %s', key)
        return self.conn.get(key)

    @staticmethod
    def url(host, port, db):
        return r'redis://' + host + r':' + str(port) + r'/' + str(db)

    def test(self):
        r = StrictRedis.from_url(url='redis://172.25.45.241:5568/0')
        print(r.execute_command('cluster slots'))

        nodes = [
            {'host': '172.25.61.74', 'port': '8147'},
            {'host': '172.25.45.241', 'port': '5568'},
            {'host': '172.25.45.240', 'port': '5590'}
        ]
        pool = ClusterConnectionPool(startup_nodes=nodes)
        rc = StrictRedisCluster(connection_pool=pool, decode_responses=True)
        print(rc.scan(cursor=0, match='*', count=100))
