from fastapi import APIRouter, Depends, Query, status
from models.responses.apiResponse import ApiResponse
from models.entities.event import Event
from data.eventRepository import EventRepository
from typing import Optional, Dict, Any
from models.exceptions.apiExceptions import ItemNotFoundException, ItemNotCreatedException, ItemNotDeletedException, ItemNotUpdatedException



eventRouter = APIRouter()

@eventRouter.post("/events", status_code=status.HTTP_201_CREATED, response_model= ApiResponse)
async def insertEvent(newEvent: Event, repository: EventRepository = Depends()):
    """ Create new event"""  
    result = repository.insert(newEvent)

    if not result:
        raise ItemNotCreatedException("Event hasnt been created")
        
    return ApiResponse.createResponse().asSuccess(status.HTTP_201_CREATED)
        
    
@eventRouter.post("/events", status_code=status.HTTP_200_OK, response_model= ApiResponse)
async def getEventByDate(condition: Optional[Dict[str, Any]], 
                         offset: int = Query(0, description="How much to skip"),
                         take: int = Query(10, description="How much to take"),
                         repository: EventRepository = Depends()):
    """ Get events by criteria """
    result = repository.get(condition, offset, take)
    if not result:
        raise ItemNotFoundException("Events hasnt been found")
           
    return ApiResponse.createResponse().addContent(result).asSuccess(status.HTTP_200_OK)
    

@eventRouter.delete("/events/{id}")
async def deleteTask(id: str, repository: EventRepository = Depends()):
    """ Delete event by Id """
    result = repository.delete(id)

    if not result:
        raise ItemNotDeletedException("Event hasnt been deleted")
    
    
@eventRouter.put("/events/{id}")
async def updateTask(id: str, changes: Event, repository: EventRepository = Depends()):
    """ Update event by Id """
    result = repository.update(id, changes)
    
    if not result:
        raise ItemNotUpdatedException("Event hasnt been updated")
