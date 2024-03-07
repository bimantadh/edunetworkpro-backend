from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
import datetime
from api.v1.base.base import BaseModel



class Application(BaseModel):
    consultancy_id = Column(int)
    university_id =Column(int)
    course_id=Column(int)
    
