__author__ = 'rock'

import json
import logging

import constants


class DictCode():
    def __init__(self):
        self.__init__()

    @staticmethod
    def do(value=None):
        logging.debug('org value is ' + str(type(value)))
        if value:
            value = json.loads(value, encoding=constants.CHARSET)
        else:
            value = 'value is nil'
        logging.debug('parse value is ' + str(type(value)))
        return value


# MAP = {}
MAP = {ur'(DICT_CODE_\d)': DictCode()}
