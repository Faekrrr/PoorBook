from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional

class ItemBase(BaseModel):
    """ Basic item model. """
    name: str 
    description: Optional[str]
    location: str
    locationDetails: str
    quantity: Optional[int] = 1
    
    @field_validator('quantity')
    def validateQuantity(cls, value):
        """ Validate quantity value """
        if value < 0:
            raise ValueError("Quantity cannot be lower than 0.")
        return value
    
class CreateItemModel(ItemBase):
    """ Request model to create new item. """
    pass

class ItemModel(ItemBase):
    """ Item object model. """
    created: datetime = Field(default_factory=datetime.now)