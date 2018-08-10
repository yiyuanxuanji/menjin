# -*- coding: utf-8 -*-
from fangkexitong import db
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

engine = db.create_engine("mssql+pymssql://visitor:12345678@cnspec.myds.me:61433/visitor", encoding='utf-8', echo=True)   # 数据库
Base = declarative_base()   # 生成SQLORM基类
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
DBSession = sessionmaker(bind=engine)
session = DBSession()