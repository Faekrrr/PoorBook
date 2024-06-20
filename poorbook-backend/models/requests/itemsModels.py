from pydantic import BaseModel
from typing import Optional

class ItemByLocationModel(BaseModel):
    """ Request model to get items by loation. """
    location: str
    
class ItemByConditionModel(BaseModel):
    """ Request model to get items by condition. """
    name: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    locationDetails: Optional[str] = None
    quantity: Optional[int] = None