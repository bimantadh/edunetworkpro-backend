from pydantic import BaseModel
import datetime

class UniversityCreate(BaseModel):
    code:str
    name: str
    description: str
    country: str
    location: str
    address: str
    website: str
    type: str
    bachelors_fee: int
    masters_fee: int
    exams: str
    established: str
    icon: str
    school_id: int
    data: str


class UniversityDetails(BaseModel):
    name: str
    country: str
    website : str
    bachelors_fee: int
    masters_fee: int
    

class CourseCreate(BaseModel):
    code: str
    name: str
    description: str
    level: str
    duration: str
    fee: int
    exams: str
    data: str
    detail_data: str

    