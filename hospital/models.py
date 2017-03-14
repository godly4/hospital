#coding: utf-8
# Database
# created: 2017-03-14
# author: dlgao

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine("mysql://igsnrr:igsnrr@localhost/db_igsnrr?charset=utf8")

class Hospital(Base):
    __tablename__ = "tb_hospital"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    province = Column(String(255))
    city = Column(String(255))
    district = Column(String(255))
    address = Column(String(255))
    phone = Column(String(255))
    category = Column(String(255))
    label = Column(String(255))
    groundpos = Column(String(255))
    marspos = Column(String(255))
    baidupos = Column(String(255))

    def __init__(self, n, p, c, d, a, ph, ca, l, g, m, b):
        self.name = n
        self.province = p
        self.city = c
        self.district = d
        self.address = a
        self.phone = ph
        self.category = ca
        self.label = l
        self.groundpos = g
        self.marspos = m
        self.baidupos = b

    def __repr__(self):
        return "<Hosiptal(id='%s', name='%s')>" % (self.id, self.name)

if __name__ == "__main__":
    Base.metadata.create_all(engine)
