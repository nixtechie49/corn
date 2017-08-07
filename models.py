# encoding:utf-8

from sqlalchemy import Column, INTEGER, SMALLINT, String
from sqlalchemy.ext.declarative import declarative_base

__author__ = 'rock'

Base = declarative_base()


class ConnInfo(Base):
    __tablename__ = 'CONN_INFO'

    id = Column(name='ID', type_=INTEGER(), primary_key=True)
    url = Column(name='URL', type_=String(256), unique=True, nullable=False)
    host = Column(name='HOST', type_=String(256), nullable=False)
    port = Column(name='PORT', type_=INTEGER(), nullable=False)
    db = Column(name='DB', type_=SMALLINT(), nullable=False)

    def __init__(self, id=None, url=None, host=None, port=None, db=None):
        self.id = id
        self.url = url
        self.host = host
        self.port = port
        self.db = db

    def __repr__(self):
        return "<ConnInfo(id='%d',url='%s',host='%s',port='%d',db='%d')>" % (
            self.id, self.url, self.host, self.port, self.db)
