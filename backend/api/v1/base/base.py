from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from db.base_class import Base


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True,autoincrement=True)
    date_created = Column(DateTime, default=datetime.utcnow)
    date_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
