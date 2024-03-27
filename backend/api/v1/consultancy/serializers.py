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

class StudentDashboard(BaseModel):
    applications_submitted : int
    applications_in_progress: int 
    applications_accepted : int
    applications_rejected: int
    connected_consultancies : int

class ConsultancyDashboard(BaseModel):
    student_counseled : int
    applications_in_progress : int
    sucessful_placements : int

class CreateNotes(BaseModel):
    note: str
    message : str

class CreateReminder(BaseModel):
    reminder :str
    message : str

class CreateNotification(BaseModel):
    message : str
    notification_from : str
    student_name : str
    type : str

class ShowNotification(BaseModel):
    message : str
    notification_from : str
    student_name : str
    type : str