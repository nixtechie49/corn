# encoding:utf-8

import logging
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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


def insert(data):
    logging.debug('insert new data %s', data)
    session = DBSession()
    session.add(data)
    session.commit()
    session.close()


def query(cls, *criterion):
    logging.debug('query data by : %s', criterion)
    session = DBSession()
    q = session.query(cls)
    if criterion:
        q = q.filter(*criterion)
    session.close()
    return q.all()
