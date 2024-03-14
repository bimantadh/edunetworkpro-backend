from pydantic import BaseModel
from typing import Optional


class UploadedFile(BaseModel):
    name :str 
    file_type : str
    mime_type : str