from fastapi import APIRouter, Depends, HTTPException, Query, status
from models.responses.apiResponse import ApiResponse
from models.entities.event import Event
from data.eventRepository import EventRepository
from typing import Optional, Dict, Any


eventRouter = APIRouter()

@eventRouter.post("/events", status_code=status.HTTP_201_CREATED, response_model= ApiResponse)
async def insertEvent(newEvent: Event, repository: EventRepository = Depends()):
    try:
        if newEvent is None or not isinstance(newEvent, Event):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid input data.")
        
        result = repository.insert(newEvent)

        if not result:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Operation failed")
        
        return ApiResponse.createResponse().asSuccess(status.HTTP_201_CREATED)
        
    except Exception as ex:
        return ApiResponse.createResponse().asError(ex)
    
@eventRouter.post("/events", status_code=status.HTTP_200_OK, response_model= ApiResponse)
async def getEventByDate(condition: Optional[Dict[str, Any]], 
                         offset: int = Query(0, description="How much to skip"),
                         take: int = Query(10, description="How much to take"),
                         repository: EventRepository = Depends()):
    """ Get events by criteria """
    try:
        result = repository.get(condition, offset, take)

        if result is None or len(result) == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Events not found")
        
        return ApiResponse.createResponse().addContent(result).asSuccess(status.HTTP_200_OK)
    
    except Exception as ex:
        return ApiResponse.createResponse().asError(ex)
    

@eventRouter.delete("/events/{id}")
async def deleteTask(id: str, repository: EventRepository = Depends()):
    """ Delete event by Id """
    try:
        result = repository.delete(id)

        if not result:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tasks hasnt been deleted")
    
    except Exception as ex:
        return ApiResponse.createResponse().asError(ex)
    
    
@eventRouter.put("/events/{id}")
async def updateTask(id: str, changes: Event, repository: EventRepository = Depends()):
    """ Update event by Id """
    try:
        result = repository.update(id, changes)

        if not result:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tasks hasnt been updated")

    except Exception as ex:
        return ApiResponse.createResponse().asError(ex)