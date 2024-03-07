from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
import datetime
from api.v1.base.base import BaseModel




class Consultancy(BaseModel):
    name = Column(String(100), primary_key=True)
    description = Column(String(500))
    address = Column(String(100))
    phone = Column(String(15))
    email = Column(String(100), unique=True, nullable=False)
    webisite = Column(String(100))
    data = Column(String(50))




