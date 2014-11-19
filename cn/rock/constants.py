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
DEFAULT_TIME = 3
CHARSET = 'utf-8'
DBS = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15')

LOG_FORMAT = "[%(asctime)s]-[%(levelname)s] : %(message)s [from %(module)s.%(funcName)s.%(lineno)d]"