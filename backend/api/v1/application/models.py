from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
import datetime
from api.v1.base.base import BaseModel



class Application(BaseModel):
    __tablename__ = 'application'
    consultancy_name = Column(String(50))
    university_name =Column(String(50))
    course_name=Column(String(50))
    status = Column(String(50))
    

