from api.v1.base.base import BaseModel
from sqlalchemy import Column, Integer, String, DateTime, Boolean


class University(BaseModel):
    code = Column(String(100), primary_key=True)
    name = Column(String(500))
    description = Column(String(100))
    country = Column(String(15))
    loacation = Column(String(100), unique=True, nullable=False)
    address = Column(String(100))
    website = Column(String(50))
    bachelors_fee = Column(Integer(20))
    masters_fee = Column(Integer(20))
    exam = Column(String(50))
    established_data = Column(String(50))
