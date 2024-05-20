from pydantic import BaseModel
from datetime import datetime


class Note(BaseModel):
    """ Note model """
    content: str
    created: datetime

