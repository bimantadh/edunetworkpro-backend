from pydantic import BaseModel
import datetime
from typing import Optional


class ConsultancyDetails(BaseModel):
    name : str
    address : Optional[str]=None
    phone :str
    website: Optional[str]=None

class StudentConsultancy(BaseModel):
    student_name :str
    country_name :str
    university_applied : str
    phone : str
