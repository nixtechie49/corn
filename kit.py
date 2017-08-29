# encoding:utf-8
import json
import os

from models import Base

__author__ = 'rock'

ROOT_PATH = os.path.join(os.path.dirname(__file__), './')
CONFIG_DIR_PATH = os.path.join(ROOT_PATH, 'config/')
TEMPLATE_DIR_PATH = os.path.join(ROOT_PATH, 'templates/')
STATIC_DIR_PATH = os.path.join(ROOT_PATH, 'static/')

LOG_FORMAT = "[%(asctime)s]-[%(levelname)s] : %(message)s [from %(module)s.%(funcName)s.%(lineno)d]"


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
