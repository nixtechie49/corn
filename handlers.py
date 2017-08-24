# encoding:utf-8

import json
import time

from tornado.web import RequestHandler

import cache
import connection
import kit
import sql
from models import ConnInfo

__author__ = 'rock'


class HomeHandler(RequestHandler):
    def get(self):
        self.render('hello.html')


class KeyHandler(RequestHandler):
    def get(self, conn_id):
        kit.debug('get conn:%s', conn_id)
        stamp = self.get_argument(name='stamp', default='0')
        match = self.get_argument(name='match', default='*')
        stamp = conn_id + '_' + match + '_' + stamp.split('_')[-1]
        kit.debug(stamp)
        count = 100
        if stamp in cache.iterator:
            it = cache.iterator[stamp]
        else:
            stamp = conn_id + '_' + match + '_' + str(int(round(time.time() * 1000)))
            conn = connection.take(conn_id)
            it = conn.scan_iter(match=match, count=count)
            cache.iterator[stamp] = it
        keys = []
        i = 0
        while i < count:
            try:
                keys.append(next(it))
                i += 1
            except StopIteration:
                kit.debug('iter stop,delete cache key:%s', stamp)
                del cache.iterator[stamp]
                stamp = '-1'
                break
        kit.debug('load keys:%s', keys)
        self.write(kit.get_success((stamp, keys)))


class ValueHandler(RequestHandler):
    def get(self, conn_id, key):
        kit.debug('load value by key: %s', key)
        r = connection.take(conn_id)
        t = r.type(key)
        kit.debug('load key type: %s', t)
        v = r.get(t, key)
        kit.debug('load key : %s', v)
        data = self.pack_data(t, v)
        kit.debug('load value (%s):%s', key, data)
        self.write(kit.get_success((t, data)))

    def str_data(self, s):
        return str(s, encoding='utf-8')

    def list_data(self, l):
        data = []
        for v in l:
            data.append(str(v, encoding='utf-8'))
        return data

    def set_data(self, s):
        data = []
        for v in s:
            data.append(str(v, encoding='utf-8'))
        return data

    def sorted_set_data(self, s):
        data = []
        for v in s:
            data.append(str(v, encoding='utf-8'))
        return data

    def hash_data(self, m):
        data = {}
        for h in m:
            k = str(h, encoding='utf-8')
            v = str(m[h], encoding='utf-8')
            data[k] = v
        return data

    __data_map__ = {
        b'string': str_data,
        b'list': list_data,
        b'set': set_data,
        b'zset': sorted_set_data,
        b'hash': hash_data,
    }

    def pack_data(self, t, v):
        if v:
            data = ValueHandler.__data_map__[t](self, v)
        else:
            data = b'nil'
        return data


class ConnectionHandler(RequestHandler):
    def post(self, *args, **kwargs):
        kit.debug('args: %s', self.request.body)
        conn = json.loads(str(self.request.body, encoding='utf-8'))
        sql.add_connection(conn)
        self.write(kit.get_success())

    def get(self):
        data = sql.query(ConnInfo)
        self.write(kit.get_success(data))


class ConnHandler(RequestHandler):
    def get(self, conn_id):
        self.write(kit.get_success())
