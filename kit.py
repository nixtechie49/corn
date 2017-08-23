# encoding:utf-8
import json
import logging
import os
import re

from models import Base

__author__ = 'rock'

ROOT_PATH = os.path.join(os.path.dirname(__file__), './')
CONFIG_DIR_PATH = os.path.join(ROOT_PATH, 'config/')
TEMPLATE_DIR_PATH = os.path.join(ROOT_PATH, 'templates/')
STATIC_DIR_PATH = os.path.join(ROOT_PATH, 'static/')

LOG_FORMAT = "[%(asctime)s]-[%(levelname)s] : %(message)s [from %(module)s.%(funcName)s.%(lineno)d]"


def log_level(level):
    return level <= logging.getLogger().getEffectiveLevel()


def debug(*args):
    if log_level(logging.DEBUG):
        logging.debug(*args)


def info(*args):
    if log_level(logging.INFO):
        logging.info(*args)


def warning(*args):
    if log_level(logging.WARNING):
        logging.warning(*args)


def error(*args):
    if log_level(logging.ERROR):
        logging.error(*args)


def json_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    elif isinstance(obj, bytes):
        return str(obj, 'utf-8')
    elif isinstance(obj, Base):
        return obj.as_dict()
    else:
        return str(obj)


def get_success(data=None):
    return json.dumps({'code': 1, 'data': data}, default=json_handler)


def get_fail(msg):
    return json.dumps({'code': 0, 'msg': msg}, default=json_handler)


if __name__ == "__main__":
    p = re.compile(r'[\S]*')
    m = re.match(p, 'dh_00,0_media_0_20170811_107')
    if m:
        print(m.group())
    else:
        print('None')
