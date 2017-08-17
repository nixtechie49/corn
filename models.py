# encoding:utf-8

from sqlalchemy import Column, INTEGER, SMALLINT, String
from sqlalchemy.ext.declarative import declarative_base

__author__ = 'rock'

Base = declarative_base()


class ConnInfo(Base):
    __tablename__ = 'CONN_INFO'

    id = Column(name='ID', type_=INTEGER(), primary_key=True)
    name = Column(name='NAME', type_=String(256), unique=True, nullable=False)
    """
    连接类型
        1 Redis
            password 密码，host 主机地址，port 端口， db 连接库，path None
        2 Redis Cluster
            password 密码，host "[{'host':'127.0.0.1','port':6379}]"，port None， db None， path None
        3 zookeeper 
            password None，host '127.0.0.1:2181,127.0.0.1:2181'，port None， db None， path zk路径 
    """
    type = Column(name='TYPE', type_=SMALLINT(), nullable=False, default=0)
    password = Column(name='PWD', type_=String(256), nullable=True)
    host = Column(name='HOST', type_=String(1024), nullable=False)
    port = Column(name='PORT', type_=INTEGER(), nullable=True)
    db = Column(name='DB', type_=SMALLINT(), nullable=True)
    path = Column(name='PATH', type_=String(256), nullable=True)

    def __init__(self, id=None, name=None, host=None, port=None, db=None):
        self.id = id
        self.name = name
        self.host = host
        self.port = port
        self.db = db

    def __repr__(self):
        return "<ConnInfo(id='%d',name='%s',host='%s',port='%d',db='%d')>" % (
            self.id, self.name, self.host, self.port, self.db)
