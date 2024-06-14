from fastapi import APIRouter, Depends, Query, status
from models.responses.apiResponse import ApiResponse
from models.entities.event import CreateEventModel, Event
from models.app.conditionModel import ConditionModel
from models.requests.eventsModels import EventsByMonthModel, EventsByRangeModel, EventsByConditionModel
from data.eventRepository import EventRepository
from typing import Optional
from models.exceptions.apiExceptions import ItemNotCreatedException, ItemNotDeletedException, ItemNotUpdatedException

eventRouter = APIRouter()

@eventRouter.post("/events", response_model= ApiResponse,
                  summary="Create new event.",
                  description="Create new event using Event model.",
                  tags=["Events"])
async def insertEvent(newEvent: CreateEventModel, repository: EventRepository = Depends()):
    """ Create new event"""  
    result = repository.insert(Event(
        eventName=newEvent.eventName,
        eventDate=newEvent.eventDate,
        eventPlace=newEvent.eventPlace
    ))

    if not result:
        raise ItemNotCreatedException("Event hasnt been created")
        
    return ApiResponse.createResponse().addContent(result).asSuccess(status.HTTP_201_CREATED)

@eventRouter.get("/events", response_model=ApiResponse,
                 summary="Get all events.",
                 description="Get all events with pagination. Default: Top 10 events, sorted by eventDate ascending.",
                 tags=["Events"])
async def getEvents(offset: int = Query(0, description="How much to skip"),
                    take: int = Query(10, description="How much to take"),
                    order: str = Query("ASC", description="How to order (ASC/DESC)"),
                    sortBy: str = Query("eventDate", description="What property to sort by"),
                    repository: EventRepository = Depends()):
    """ Get all events """
    result = repository.getSorted(ConditionModel(
        take=take,
        offset=offset,
        sortOrder=order,
        sortBy=sortBy
    ))
    
    return ApiResponse.createResponse().addContent(result).asSuccess(status.HTTP_200_OK)

@eventRouter.post("/events/month", response_model=ApiResponse,
                  summary="Get all events from given month",
                  description="Get all events by month and year. Month should be formatted as string like 'March' and year like '2024'",
                  tags=["Events"])
async def getEventsByMonth(condition: EventsByMonthModel,
                           offset: int = Query(0, description="How much to skip"),
                           take: int = Query(10, description="How much to take"),
                           order: str = Query("ASC", description="How to order (ASC/DESC)"),
                           sortBy: str = Query("eventDate", description="Which property to sort by"),
                           repository: EventRepository = Depends()):
    """ Get events by month """
    result = repository.getMonth(ConditionModel(
        take=take,
        offset=offset,
        sortOrder=order,
        sortBy=sortBy
    ), 
    month=condition.month,
    year=condition.year)
    
    return ApiResponse.createResponse().addContent(result).asSuccess(status.HTTP_200_OK)

@eventRouter.post("/events/range", response_model=ApiResponse,
                  summary="Get events by date range.",
                  description="Get events by range (datetime range)",
                  tags=["Events"])
async def getEventsByRange(condition: EventsByRangeModel,
                           offset: int = Query(0, description="How much to skip"),
                           take: int = Query(10, description="How much to take"),
                           order: str = Query("ASC", description="How to order (ASC/DESC)"),
                           sortBy: str = Query("eventDate", description="Which property to sort by"),
                           repository: EventRepository = Depends()):
    """ Get events based on data range """
    result = repository.getRange(ConditionModel(
        take=take,
        offset=offset,
        sortOrder=order,
        sortBy=sortBy
    ),
    range=condition)
    
    return ApiResponse.createResponse().addContent(result).asSuccess(status.HTTP_200_OK)
        
@eventRouter.post("/events/condition", response_model=ApiResponse, 
                  summary="Get events by criteria.", 
                  description="""Retrieve events based on specific filtering and sorting criteria. 
                  All conditions are optional and body can be empty.""",
                  tags=["Events"])
async def getEventsByCondition(condition: Optional[EventsByConditionModel],
                              offset: int = Query(0, description="How much to skip"),
                              take: int = Query(10, description="How much to take"),
                              order: str = Query("ASC", description="How to order (ASC/DESC)"),
                              sortBy: str = Query("eventDate", description="Which property to sort by"),
                              repository: EventRepository = Depends()):
    """ Get events by criteria """
    result = repository.getSorted(ConditionModel(
        take=take,
        offset=offset,
        condition=condition.dict(),
        sortOrder=order,
        sortBy=sortBy   
    ))
 
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
