# encoding:utf-8
import logging
import os

__author__ = 'rock'

ROOT_PATH = os.path.join(os.path.dirname(__file__), './')
CONFIG_DIR_PATH = os.path.join(ROOT_PATH, 'config/')
TEMPLATE_DIR_PATH = os.path.join(ROOT_PATH, 'templates/')
STATIC_DIR_PATH = os.path.join(ROOT_PATH, 'static/')

LOG_FORMAT = "[%(asctime)s]-[%(levelname)s] : %(message)s [from %(module)s.%(funcName)s.%(lineno)d]"


def log_level(level):
    return level <= logging.getLogger().getEffectiveLevel()


def date_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    elif isinstance(obj, bytes):
        return str(obj, 'utf-8')
    else:
        return str(obj)
