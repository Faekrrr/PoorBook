from pydantic import BaseModel
from datetime import datetime


class Note(BaseModel):
    """ Note model """
    noteContent: str
    noteCreated: datetime = datetime.now()

