from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
import datetime
from api.v1.base.base import BaseModel
from sqlalchemy.orm import relationship

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
import datetime
from api.v1.base.base import BaseModel
from sqlalchemy.orm import relationship

class Consultancy(BaseModel):
    __tablename__ = 'consultancy'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    address = Column(String(100), nullable=True)
    phone = Column(String(15))
    email = Column(String(100), unique=True, nullable=False)
    website = Column(String(100), nullable=True)
    data = Column(String(50), nullable=True)
    university_id = Column(Integer, ForeignKey('university.id'))

    university = relationship('University', back_populates='consultancies')




