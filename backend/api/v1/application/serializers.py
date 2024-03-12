from pydantic import BaseModel
import datetime

class ApplicationCreate(BaseModel):
    consultancy_id : int
    university_id : int
    course_id : int
    status : str
