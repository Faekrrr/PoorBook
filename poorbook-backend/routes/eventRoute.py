from fastapi import APIRouter, Depends, Query, status
from models.responses.apiResponse import ApiResponse
from models.entities.event import Event
from models.app.getCondition import GetCondition
from data.eventRepository import EventRepository
from typing import Optional, Dict, Any
from models.exceptions.apiExceptions import ItemNotFoundException, ItemNotCreatedException, ItemNotDeletedException, ItemNotUpdatedException

eventRouter = APIRouter()

@eventRouter.post("/events", response_model= ApiResponse,
                  summary="Create new event.",
                  description="Create new event using Event model.",
                  tags=["Events"])
async def insertEvent(newEvent: Event, repository: EventRepository = Depends()):
    """ Create new event"""  
    result = repository.insert(newEvent)

    if not result:
        raise ItemNotCreatedException("Event hasnt been created")
        
    return ApiResponse.createResponse().asSuccess(status.HTTP_201_CREATED)

@eventRouter.get("/events", response_model=ApiResponse,
                 summary="Get all events.",
                 description="Get all events with pagination.",
                 tags=["Events"])
async def getEvents(offset: int = Query(0, description="How much to skip"),
                    take: int = Query(10, description="How much to take"),
                    order: str = Query("ASC", description="How to order"),
                    sortBy: str = Query("eventDate", description="What property to sort by"),
                    repository: EventRepository = Depends()):
    """ Get all events """
    result = repository.getSorted(GetCondition(
        take=take,
        offset=offset,
        sortOrder=order,
        sortBy=sortBy
    ))
    
    if not result:
        raise ItemNotFoundException("No events found.")

    return ApiResponse.createResponse().addContent(result).asSuccess(status.HTTP_200_OK)
        
    
@eventRouter.post("/events/condition", response_model= ApiResponse, 
                  summary="Get events by criteria.", 
                  description="Retrieve events based on specific filtering and sorting criteria.",
                  tags=["Events"])
async def getTasksByCondition(condition: Optional[Dict[str, Any]],
                              offset: int = Query(0, description="How much to skip"),
                              take: int = Query(10, description="How much to take"),
                              order: str = Query("ASC", description="How to order"),
                              sortBy: str = Query("eventDate", description="Which property to sort by"),
                              repository: EventRepository = Depends()):
    """ Get events by criteria """
    result = repository.getSorted(GetCondition(
        take=take,
        offset=offset,
        condition=condition,
        sortOrder=order,
        sortBy=sortBy   
    ))

    if not result:
        raise ItemNotFoundException("No events found.")
        
    return ApiResponse.createResponse().addContent(result).asSuccess(status.HTTP_200_OK)
    

@eventRouter.delete("/events/{id}", 
                    summary="Delete event by Id.",
                    description="Delete event providing event Id.",
                    tags=["Events"])
async def deleteEvent(id: str, repository: EventRepository = Depends()):
    """ Delete event by Id """
    result = repository.delete(id)

    if not result:
        raise ItemNotDeletedException("Event hasnt been deleted")
    
@eventRouter.put("/events/{id}", 
                    summary="Update event by Id.",
                    description="Update event providing event Id.",
                    tags=["Events"])
async def updateEvent(id: str, changes: Event, repository: EventRepository = Depends()):
    """ Update event by Id """
    result = repository.update(id, changes)
    
    if not result:
        raise ItemNotUpdatedException("Event hasnt been updated")
