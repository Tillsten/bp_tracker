# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 03:44:09 2015

@author: Tillsten
"""

from sqlalchemy import Column, Integer, String, DateTime, Enum
from database import Base
import datetime

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)
    password = Column(String(10))

    def __init__(self, name=None, email=None, password=None):
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % (self.name)


class Entry(Base):
    __tablename__ = 'entrys'
    id = Column(Integer, primary_key=True)
    sys = Column(Integer)
    dia = Column(Integer)
    pulse = Column(Integer)
    date = Column(DateTime)
    arm_side = Column(Enum('left', 'right'))
    when = Column(Enum('after_sleep', 'before_sleep'))

    def __init__(self, sys, dia, pulse, arm_side, when):
        self.date = datetime.datetime.utcnow()
        self.sys = sys
        self.dia = dia
        self.pulse = pulse
        self.arm_side = arm_side
        self.when = when



