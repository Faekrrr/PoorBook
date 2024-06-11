from pydantic import BaseModel, model_validator, field_validator
from datetime import datetime
import calendar


class CreateEvent(BaseModel):
    """ Create event model """
    eventName: str
    eventDate: datetime
    eventPlace: str
    
    @field_validator("eventName")
    def validateEventName(cls, value):
        """ Validate event name len """
        MAX_NAME_LEN = 255
        if len(value) > MAX_NAME_LEN:
            raise ValueError("Event name is too long")
        return value

class Event(CreateEvent):
    """ Event entity """
    eventCreated: datetime = datetime.now()
    eventMonth: str = None
    eventYear: int = None

    @model_validator(mode='before')
    def setEventMonth(cls, values):
        """ Sets eventMonth based on given date """
        eventDate = values.get('eventDate')
        if eventDate:
            if isinstance(eventDate, str):
                eventDate = datetime.fromisoformat(eventDate)
            values['eventMonth'] = calendar.month_name[eventDate.month]
        return values

    @model_validator(mode='before')
    def setEventYear(cls, values):
        """ Sets evenYear based on given date """
        eventDate = values.get('eventDate')
        if eventDate:
            if isinstance(eventDate, str):
                eventDate = datetime.fromisoformat(eventDate)
            values['eventYear'] = eventDate.year
        return values

    
