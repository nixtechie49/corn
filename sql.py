# encoding:utf-8

import logging
import os

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

import kit
import models
import settings

__author__ = 'rock'
table_name = 'data.db'
engine = create_engine('sqlite:///' + table_name, echo=settings.DEBUG, pool_recycle=3600)

DBSession = sessionmaker(bind=engine)


def init():
    if not os.path.exists(table_name):
        logging.info('data file not exists, creating...')
        models.ConnInfo.__table__.create(bind=engine)
        logging.info('data file created')


def add_connection(data):
    if kit.log_level(logging.DEBUG):
        logging.debug('insert new data %s', data)
    pre_sql = 'INSERT INTO CONN_INFO ' \
              '(NAME,TYPE,PWD,HOST,PORT,DB,PATH) VALUES ' \
              '(:name,:type,:password,:host,:port,:db,:path)'
    sql = text(pre_sql)
    res = engine.execute(sql, data)
    return res.lastrowid


def query(cls, *criterion):
    if kit.log_level(logging.DEBUG):
        logging.debug('query data by : %s', criterion)
    session = DBSession()
    q = session.query(cls)
    if criterion:
        q = q.filter(*criterion)
    session.close()
    result = q.all()
    if kit.log_level(logging.DEBUG):
        logging.debug('query result is : %s', result)
    return result


def get(cls, id):
    if kit.log_level(logging.DEBUG):
        logging.debug('get data id : %s', id)
    session = DBSession()
    q = session.query(cls)
    q = q.filter(id=id)
    session.close()
    result = q.fatchone()
    if kit.log_level(logging.DEBUG):
        logging.debug('get result is : %s', result)
    return result
