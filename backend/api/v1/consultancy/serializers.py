from pydantic import BaseModel
import datetime
from typing import Optional


class ConsultancyDetails(BaseModel):
    name : str
    address : Optional[str]=None
    phone :str
    website: Optional[str]=None
