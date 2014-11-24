# encoding:utf-8
__author__ = 'rock'

import os

import redis

from cn.rock import constants


try:
    import xml.etree.cElementTree as XMLParser
except ImportError:
    import xml.etree.ElementTree as XMLParser


def load_collection_config():
    """加载Collection.xml配置文件
    """
    doc = XMLParser.ElementTree(file=os.path.join(constants.CONFIG_DIR_PATH, 'collections.xml'))
    root = doc.getroot()
    constants.REDIS_CONFIG = {}
    for col in root:
        name = col.attrib['name']
        prop = {}
        for sub in col:
            prop[sub.tag] = sub.text
        save_config(name, prop)


def save_config(name, prop):
    """将collection.xml保存为dict
    """
    ip = prop['ip']
    port = prop['port']
    db = '0'
    if 'db' in prop:
        db = prop['db']
    time = constants.DEFAULT_TIME
    if 'timeout' in prop:
        time = prop['timeout']
    col = {'ip': ip, 'port': port, 'db': db, 'time': time}
    constants.REDIS_CONFIG[name] = col


def get_pool(name, db):
    location = constants.REDIS_CONFIG[name]
    key = name + '_' + db
    if not constants.REDIS_POOL.get(key):
        constants.REDIS_POOL[key] = redis.ConnectionPool(host=location['ip'], port=location['port'], db=db,
                                                         socket_timeout=location['time'])
    return constants.REDIS_POOL[key]


def get_redis(name, db='0'):
    pool = get_pool(name, db)
    return redis.Redis(connection_pool=pool)


def get_type_and_value(key, r):
    t = r.type(key)
    value = ''
    # TODO 分页
    if t == b'hash':
        value = r.hgetall(key)
    elif t == b'string':
        value = r.get(key).decode(constants.CHARSET)
    elif t == b'list':
        value = r.lrange(key, 0, -1)
    elif t == b'set':
        value = list(r.smembers(key))
    elif t == b'zset':
        value = r.zrange(key, 0, -1, withscores=True)
    return t, value


def delete(r, key):
    flag = 1
    if isinstance(key, tuple):
        flag = len(key)
    result = r.delete(key)
    return flag == result


