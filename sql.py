# encoding:utf-8

import os

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

import kit
import models

__author__ = 'rock'
table_name = 'data.db'
engine = create_engine('sqlite:///' + table_name, echo=True, pool_recycle=3600)

DBSession = sessionmaker(bind=engine)


def init():
    if not os.path.exists(table_name):
        kit.info('data file not exists, creating...')
        models.ConnInfo.__table__.create(bind=engine)
        kit.info('data file created')


def add_connection(data):
    kit.debug('insert new data %s', data)
    pre_sql = 'INSERT INTO CONN_INFO ' \
              '(NAME,TYPE,PWD,HOST,PORT,DB,PATH) VALUES ' \
              '(:name,:type,:password,:host,:port,:db,:path)'
    sql = text(pre_sql)
    res = engine.execute(sql, data)
    return res.lastrowid


def query(cls, *criterion):
    kit.debug('query data by : %s', criterion)
    session = DBSession()
    q = session.query(cls)
    if criterion:
        q = q.filter(*criterion)
    session.close()
    result = q.all()
    kit.debug('query result is : %s', result)
    return result


def get(cls, id):
    kit.debug('get data id : %s', id)
    session = DBSession()
    q = session.query(cls)
    q = q.filter('id=' + str(id))
    session.close()
    result = q.one()
    kit.debug('get result is : %s', result)
    return result
