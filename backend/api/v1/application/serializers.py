from pydantic import BaseModel
import datetime

class ApplicationCreate(BaseModel):
    consultancy_name : str
    university_name : str
    course_name : str
    status : str
