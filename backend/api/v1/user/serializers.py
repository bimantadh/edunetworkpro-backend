from pydantic import BaseModel
import datetime
class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str

       
class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str

class requestdetails(BaseModel):
    email:str
    password:str