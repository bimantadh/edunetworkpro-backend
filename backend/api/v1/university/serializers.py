from pydantic import BaseModel
import datetime

class UniversityCreate(BaseModel):
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

