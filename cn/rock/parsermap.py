__author__ = 'rock'

from abc import abstractmethod
import json
import logging

import constants


class ValueParser(object):
    @staticmethod
    @abstractmethod
    def parse(value=None):
        pass


class DictCode(ValueParser):
    @staticmethod
    def parse(value=None):
        logging.debug('org value is ' + str(type(value)))
        if value:
            value = json.loads(value, encoding=constants.CHARSET)
        else:
            value = 'value is nil'
        logging.debug('parse value is ' + str(type(value)))
        return value

# MAP = {}
MAP = {u'(DICT_CODE_\d)': DictCode()}
