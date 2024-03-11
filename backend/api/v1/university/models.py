from api.v1.base.base import BaseModel
from sqlalchemy import Column, Integer, String, DateTime, Boolean

class University(BaseModel):
    __tablename__ = "university"
    code = Column(String(50))
    name= Column(String(50))
    description=Column(String(50))
    country=Column(String(50))
    location= Column(String(50))
    address= Column(String(50))
    website= Column(String(50))
    type= Column(String(50))
    bachelors_fee= Column(Integer)
    masters_fee= Column(Integer)
    exams=Column(String(50))
    established= Column(String(50))
    icon= Column(String(50))
    school_id= Column(Integer)
    

class Course(BaseModel):
    __tablename__ = 'course'
    code = Column(String(50))
    name = Column(String(50))  
    description = Column(String(50))  
    level = Column(String(50)) 
    duration = Column(String(50))
    fee = Column(Integer)
    exams = Column(String(50)) 
    data = Column(String(50))
    detail_data = Column(String(50))

