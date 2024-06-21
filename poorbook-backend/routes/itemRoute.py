from fastapi import APIRouter, Depends, Query, status
from data.itemRepository import ItemRepository
from models.requests.itemsModels import ItemByLocationModel, ItemByConditionModel
from models.exceptions.apiExceptions import ItemNotCreatedException, ItemNotDeletedException, ItemNotUpdatedException
from models.entities.item import ItemModel, CreateItemModel
from models.responses.apiResponse import ApiResponse
from models.app.conditionModel import ConditionModel
from typing import Optional

itemRouter = APIRouter()

@itemRouter.post("/items",response_model=ApiResponse,
                  summary="Create new item.",
                  description="Create new item using Item model.",
                  tags=["Items"] )
async def insertItem(newItem: CreateItemModel, repository: ItemRepository = Depends()):
    """ Create new item. """
    result = repository.insert(ItemModel(name=newItem.name,
                                         description=newItem.description,
                                         location=newItem.location,
                                         locationDetails=newItem.locationDetails))
    if not result:
        raise ItemNotCreatedException("Item hasnt been created")
        
    return ApiResponse.createResponse().addContent(result).asSuccess(status.HTTP_201_CREATED)

@itemRouter.get("/items", response_model=ApiResponse,
                summary="Get all items. ",
                description="Get all items with pagination. Default: Top 10 order by ASC. ",
                tags=["Items"])
async def getItems(offset: int = Query(0, description="How much to skip"),
                   take: int = Query(10, description="How much to take"),
                   order: str = Query("ASC", description="How to order"),
                   sortBy: str = Query("created", description="Which property to sort by"),
                   repository: ItemRepository = Depends()):
    "Get all items"
    result = repository.getSorted(ConditionModel(
        take=take,
        offset=offset,
        sortOrder=order,
        sortBy=sortBy
    ))
    
    return ApiResponse.createResponse().addContent(result).asSuccess(status.HTTP_200_OK)

@itemRouter.post("/items/location", response_model=ApiResponse,
                 summary="Get items from certain location.",
                 description="Get all items belongs to choosen location.",
                 tags=["Items"])
async def getItemsByLocation(location: ItemByLocationModel,
                            offset: int = Query(0, description="How much to skip"),
                            take: int = Query(10, description="How much to take"),
                            order: str = Query("ASC", description="How to order"),
                            sortBy: str = Query("created", description="Which property to sort by"),
                            repository: ItemRepository = Depends()):
    """ Get items by location. """
    result = repository.getSorted(ConditionModel(
        take=take,
        offset=offset,
        filterBy={"location": location},
        sortOrder=order,
        sortBy=sortBy
    ))
    
    return ApiResponse.createResponse().addContent(result).asSuccess(status.HTTP_200_OK)


@itemRouter.post("/items/search", response_model= ApiResponse, 
                  summary="Get items by criteria.", 
                  description="Retrieve items based on specific filtering and sorting criteria.",
                  tags=["Items"])
async def getItemsByCondition(condition: Optional[ItemByConditionModel],
                              offset: int = Query(0, description="How much to skip"),
                              take: int = Query(10, description="How much to take"),
                              order: str = Query("ASC", description="How to order"),
                              sortBy: str = Query("created", description="Which property to sort by"),
                              repository: ItemRepository = Depends()):
    """ Get tasks by criteria """
    result = repository.getSorted(ConditionModel(
        take=take,
        offset=offset,
        condition=condition.model_dump(),
        sortOrder=order,
        sortBy=sortBy   
    ))
        
    return ApiResponse.createResponse().addContent(result).asSuccess(status.HTTP_200_OK)


@itemRouter.delete("/items/{id}", status_code=status.HTTP_204_NO_CONTENT,
                    summary="Delete item by Id.",
                    description="Delete item providing task Id.",
                    tags=["Items"])
async def deleteItem(id: str, repository: ItemRepository = Depends()):
    """ Delete item by Id """
    result = repository.delete(id)
    if not result:
        raise ItemNotDeletedException("Task hasnt been deleted")
    
    
@itemRouter.put("/items/{id}", status_code=status.HTTP_204_NO_CONTENT,
                 summary="Update item by Id.",
                 description="Update item providing Id and new task body.",
                 tags=["Items"])
async def updateItem(id: str, changes: ItemModel, repository: ItemRepository = Depends()):
    """ Update item by Id """
    result = repository.update(id, changes)

    if not result:
        raise ItemNotUpdatedException("Item hasnt been updated")
