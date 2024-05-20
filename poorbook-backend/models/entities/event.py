from pydantic import BaseModel, root_validator, validator
from datetime import datetime
import calendar


class Event(BaseModel):
    """ Event entity """
    eventName: str
    eventCreated: datetime
    eventDate: datetime
    eventMonth: str = None
    eventPlace: str

    @root_validator(pre=True)
    def setEventMonth(cls, values):
        """ Sets eventMonth based on given date """
        eventDate = values.get('eventDate')
        if eventDate:
            if isinstance(eventDate, str):
                eventDate = datetime.fromisoformat(eventDate)
            values['eventMonth'] = calendar.month_name[eventDate.month]
        return values


    @validator("eventName")
    def validateEventName(cls, value):
        """ Validate event name len """
        MAX_NAME_LEN = 255
        if len(value) > MAX_NAME_LEN:
            raise ValueError("Event name is too long")
        return value
