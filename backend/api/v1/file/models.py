from api.v1.base.base import BaseModel
from sqlalchemy import Column, Integer, String
from enum import Enum


class File(BaseModel):
    __tablename__ = 'files'
    name = Column(String(100), nullable=False)
    file_type = Column(String(20), nullable=False)
    mime_type = Column(String(50))