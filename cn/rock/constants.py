# encoding:utf-8
__author__ = 'rock'
import os

ROOT_PATH = os.path.join(os.path.dirname(__file__), '../../')

CONFIG_DIR_PATH = os.path.join(ROOT_PATH, 'config/')
TEMPLATE_DIR_PATH = os.path.join(ROOT_PATH, 'templates/')
STATIC_DIR_PATH = os.path.join(ROOT_PATH, 'static/')

REDIS_CONFIG = {}

REDIS_POOL = {}

CURRENT_REDIS = None
CURRENT_DB = 0
CHARSET = 'utf-8'

LOG_FORMAT = '[%(asctime)s]-[%(levelname)s]-[%(thread)d]=[%(threadName)s] : %(message)s [from %(filename)s|%(module)s|%(funcName)s]'