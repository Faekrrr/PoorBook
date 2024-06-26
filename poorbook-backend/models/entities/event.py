from pydantic import BaseModel, model_validator, field_validator, Field
from datetime import datetime
import calendar

class EventModel(BaseModel):
    """ Basic event model. """
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
    
class CreateEventModel(EventModel):
    """ Request model to create new Event. """
    pass

class Event(EventModel):
    """ Event entity """  
    eventCreated: datetime = Field(default_factory=datetime.now) 
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

