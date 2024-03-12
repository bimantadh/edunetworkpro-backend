from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
import datetime
from api.v1.base.base import BaseModel



class Application(BaseModel):
    __tablename__ = 'application'
    consultancy_id = Column(Integer)
    university_id = Column(Integer)
    course_id= Column(Integer)
    status = Column(String(50))
    

