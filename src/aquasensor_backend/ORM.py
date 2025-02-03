from functools import partial
import sqlalchemy

sqlalchemy.AdaptedConnection
from sqlalchemy import DateTime, create_engine

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timezone

engine = create_engine('sqlite:///:memory:')

Base = declarative_base()

current_utc_datetime = partial(datetime.now, timezone.utc)

class Users(Base):
    __tablename__ = 'users'
    
    uid = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

class RiverData(Base):
    __tablename__ = 'RiverData'

    RiverId = Column(Integer, primary_key=True)
    Rivertemp = Column(Integer)
    DOlevels = Column(Integer)
    updated_at = Column(DateTime, default=current_utc_datetime, onupdate=current_utc_datetime)


