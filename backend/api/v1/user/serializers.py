from pydantic import BaseModel
import datetime
class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    phone : str
    type: str

       
class TokenSchema(BaseModel):
    access: str
    token_type : str
    user_type : str

class requestdetails(BaseModel):
    email:str
    password:str

class UserDetails(BaseModel):
    first_name : str
    last_name : str
    email : str
    type : str