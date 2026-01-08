from enum import Enum
from sqlalchemy import Column, Integer, String
from .database import DBModel


class User(DBModel):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    login = Column(String(50))
    password = Column(String(256))
    name = Column(String(50))


class Client(DBModel):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    address = Column(String(50))
