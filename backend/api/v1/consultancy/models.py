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


class UniversityConsultancy(BaseModel):
    __tablename__ = 'universityconsultancy'
    university_id = Column(Integer)
    consultancy_id = Column(Integer)


class ConsultancyNotes(BaseModel):
    __tablename__ = 'note'
    note = Column(String(50))
    message = Column(String (100))
    reminder = Column(String(50))

class Notification(BaseModel):
    __tablename__ = 'notification'

    message = Column(String (100))
    notification_from= Column(String(50))
    student_name = Column(String(50))
    type = Column(String(50))
