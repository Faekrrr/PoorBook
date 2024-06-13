from pydantic import BaseModel
from typing import Optional, Any, Dict


class ConditionModel(BaseModel):
    """ Model of data needed to return item list from collection """
    offset: int 
    take: int
    condition: Optional[Dict[str, Any]] = None
    filterBy: Optional[Dict[str, Any]] = None
    sortBy: str
    sortOrder: str
    
    
