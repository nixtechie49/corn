# encoding:utf-8

import json
import logging as log

from redis import StrictRedis
from rediscluster import StrictRedisCluster
from rediscluster.connection import ClusterConnectionPool

import sql
import zk
from models import ConnInfo

__author__ = 'rock'

__conn_map__ = {}


def take(cid):
    cid = int(cid)
    log.debug('get connection = %d', cid)
    r = __conn_map__.get(cid)
    if not r:
        ci = sql.get(ConnInfo, cid)
        log.info('init redis connection<id=%d>', cid)
        r = Redis(ci)
        __conn_map__[cid] = r
    return r


def __update_address__(data, stat, event):
    pass


class Redis:
    def __init__(self, ci):
        log.debug('create connection = %s', ci)
        t = ci.type
        self.t = t
        if t == 1:
            log.debug('create redis connection.')
            self.conn = StrictRedis(host=ci.host, port=ci.port, db=ci.db)
        elif t == 2:
            log.debug('create redis cluster connection.')
            nodes = json.loads(ci.host)
            pool = ClusterConnectionPool(startup_nodes=nodes)
            self.conn = StrictRedisCluster(connection_pool=pool, decode_responses=True)
        elif t == 3:
            log.debug('create redis connection from zookeeper.')
            client = zk.Client(hosts=ci.host, read_only=True)
            node = client.get(ci.path)
            arr = str(node[0], encoding='utf-8').split('\n')
            address = []
            for h in arr:
                if h is '':
                    continue
                a = h.split(':')
                address.append({'host': a[0], 'port': int(a[1])})
            pool = ClusterConnectionPool(startup_nodes=address)
            self.conn = StrictRedisCluster(connection_pool=pool, decode_responses=True)
        else:
            raise AttributeError('illegal ConnInfo type.')
        if self.test():
            self.ci = ci
            log.info('connect redis(%s) success', ci.host)

    def test(self):
        log.debug('test connect redis(%s)', self.conn)
        good = False
        try:
            result = self.conn.ping()
            if self.t == 1:
                good = result
            else:
                for k in result:
                    v = result[k]
                    log.debug('test [%s] result : %s', k, v)
                    if not v:
                        return False
                good = True
        except Exception as e:
            log.error(e)
        finally:
            log.debug('redis connection is good[%s]', good)
        return good

    def db_size(self):
        return self.conn.dbsize()

    def scan_iter(self, match='*', count=None):
        if match is not '*':
            match = '*' + match + '*'
        return self.conn.scan_iter(match=match, count=count)

    def get_str(self, key):
        log.debug('get str value by key: %s', key)
        return self.conn.get(key)

    def l_range(self, key):
        start = 0
        end = -1
        log.debug('get list value from %d to %d by key: %s', start, end, key)
        return self.conn.lrange(key, start, end)

    def z_range(self, key):
        start = 0
        end = -1
        log.debug('get sorted set value from %d to %d by key: %s', start, end, key)
        return self.conn.zrange(key, start, end)

    def s_members(self, key):
        log.debug('get set value by key: %s', key)
        return self.conn.smembers(key)

    def h_get_all(self, key):
        log.debug('get hash value by key: %s', key)
        return self.conn.hgetall(key)

    def get(self, t, k):
        f = self.__t_f_map__[t]
        return f(self, k)

    def type(self, key):
        log.debug('get type by key: %s', key)
        return self.conn.type(key)

    __t_f_map__ = {
        b'string': get_str,
        b'list': l_range,
        b'set': s_members,
        b'zset': z_range,
        b'hash': h_get_all,
    }
