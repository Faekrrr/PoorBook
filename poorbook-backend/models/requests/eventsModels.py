from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EventsByMonthModel(BaseModel):
    """ Requst model to get events by it's month. """
    month: str
    year: int
    
class EventsByRangeModel(BaseModel):
    """ Request model to get events by its date range. """
    dateFrom: datetime
    dateTo: datetime
    
class EventsByConditionModel(BaseModel):
    """ Request model to get events passing conditions. """
    eventName: Optional[str] = None
    eventDate: Optional[datetime] = None
    eventMonth: Optional[str] = None
    eventYear: Optional[int] = None
    eventCreated: Optional[datetime ]= None
    eventPlace: Optional[str] = None