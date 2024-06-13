from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EventsByMonthModel(BaseModel):
    """ Get events by month request. """
    month: str
    year: int
    
class EventsByRangeModel(BaseModel):
    """ Get events by date range. """
    dateFrom: datetime
    dateTo: datetime
    
class EventsByConditionModel(BaseModel):
    """ Get events by conditions """
    eventName: Optional[str] = None
    eventDate: Optional[datetime] = None
    eventMonth: Optional[str] = None
    eventYear: Optional[int] = None
    eventCreated: Optional[datetime ]= None
    eventPlace: Optional[str] = None