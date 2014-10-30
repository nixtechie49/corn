# encoding:utf-8
__author__ = 'rock'

import os

import redis

from cn.rock import constants


try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


def loadConllectionsConfig():
    """加载Conllection.xml配置文件
    """
    doc = ET.ElementTree(file=os.path.join(constants.CONFIG_DIR_PATH, 'collections.xml'))
    root = doc.getroot()
    constants.REDIS_CONFIG = {}
    for col in root:
        name = col.attrib['name']
        property = {}
        for sub in col:
            property[sub.tag] = sub.text
        saveconfig(name, property)


def saveconfig(name, property):
    """将collection.xml保存为dict
    """
    ip = property['ip']
    port = property['port']
    db = property['db']
    if not db:
        db = '0'
    col = {'ip': ip, 'port': port, 'db': db}
    constants.REDIS_CONFIG[name] = col


def getPool(name, db):
    location = constants.REDIS_CONFIG[name]
    key = name + '_' + db
    if not constants.REDIS_POOL.get(key):
        constants.REDIS_POOL[key] = redis.ConnectionPool(host=location['ip'], port=location['port'], db=db)
    return constants.REDIS_POOL[key]


def getRedis(name, db='0'):
    pool = getPool(name, db)
    return redis.Redis(connection_pool=pool)


def getValue(key, r):
    type = r.type(key)
    print(type)
    value = ''
    # TODO 分页
    if type == b'hash':
        value = r.hgetall(key)
    elif type == b'string':
        value = r.get(key).decode(constants.CHARSET)
    elif type == b'list':
        value = r.lrange(key, 0, -1)
    elif type == b'set':
        value = r.smembers(key)
    elif type == b'zset':
        value = r.zrange(key, 0, -1)
    return value



