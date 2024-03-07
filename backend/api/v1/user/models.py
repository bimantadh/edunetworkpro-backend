from sqlalchemy import Column, Integer, String
from api.v1.base.base import BaseModel

class User(BaseModel):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(100), unique=True)
    password = Column(String(100))
    type = Column(String(100))

class userroles(BaseModel):
    __tablename__ = 'userroles'
    