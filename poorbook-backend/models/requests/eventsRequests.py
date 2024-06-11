from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class GetEventByMonth(BaseModel):
    """ Get event by month request """
    month: str
    year: int
    
class GetEventByRange(BaseModel):
    """ Get event by date range """
    dateFrom: datetime
    dateTo: datetime
    
class GetEventByCondition(BaseModel):
    """ Get events by conditions """
    eventName: Optional[str] = None
    eventDate: Optional[datetime] = None
    eventMonth: Optional[str] = None
    eventYear: Optional[int] = None
    eventCreated: Optional[datetime ]= None
    eventPlace: Optional[str] = None