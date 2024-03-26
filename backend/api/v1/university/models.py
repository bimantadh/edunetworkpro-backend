from api.v1.base.base import BaseModel
from sqlalchemy import Column, Integer, String, DateTime, Boolean,ForeignKey
from sqlalchemy.orm import relationship


from sqlalchemy import Column, Integer, String
from api.v1.base.base import BaseModel
from sqlalchemy.orm import relationship

class University(BaseModel):
    __tablename__ = 'university'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    code = Column(String(50))
    description = Column(String(500))
    country = Column(String(50))
    location = Column(String(100))
    address = Column(String(100))
    website = Column(String(100))
    type = Column(String(50))
    bachelors_fee = Column(Integer)
    masters_fee = Column(Integer)
    exams = Column(String(100))
    established = Column(String(50))
    icon = Column(String(100))
    school_id = Column(Integer)

    consultancies = relationship('Consultancy', back_populates='university')

    

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


class UniversityProgram(BaseModel):
    __tablename__ = 'universityprogram'
    university_id = Column(Integer)
    code = Column(Integer)
    program = Column(String(50))
    program_id = Column(Integer)
    data = Column(String(50))
    programcourses = Course








