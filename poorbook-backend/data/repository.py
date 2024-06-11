from data.connection import Connection
from mappers.genericMapper import genericMapper, genericSerialMapper
from models.exceptions.apiExceptions import InvalidOrderException
from models.enums.sortedBy import SortedBy
from bson import ObjectId
from typing import Optional, Any, Dict
from models.app.getCondition import GetCondition


class Repository():
    """ Entity repository """
    def __init__(self, collectionName: str) -> None:
        self._conection = Connection()
        self._database = self._conection.database
        self._collection = self._database[collectionName]


    def insert (self, entityToAdd) -> bool:
        """ Insert new entity"""
        result = self._collection.insert_one(genericMapper(entityToAdd.model_dump()))
        return result.inserted_id is not None
    
    def delete(self, entityId: str) -> bool:
        """ Delete entity by ID"""
        result = self._collection.delete_one({"_id": ObjectId(entityId)})
        return result.deleted_count == 1
    
    def update (self, entityId, changes) -> bool:
        """ Update item of given Id by new data"""
        result = self._collection.update_one({"_id": ObjectId(entityId)}, {"$set": dict(changes)})
        return result.modified_count > 0
    
    def get(self, offset: int, take: int, condition: Optional[Dict[str, Any]] = {}):
        """ Get items by given criteria """
        if condition is None or condition == {}:
            cursor = self._collection.find()
            
        else:
            cursor = self._collection.find(condition)

        cursor = cursor.skip(offset).limit(take)
        result = list(cursor)
        return genericSerialMapper(result) if result else None
    
    def getSorted(self, condition: GetCondition):
        """ Get sorted items """
        searchCondition = {}

        if condition.filterBy:
            searchCondition.update(condition.filterBy)
            
        if condition.condition:
            searchCondition.update(condition.condition)

        orderBy = self._getOrderFromString(condition.sortOrder)

        cursor = self._collection.find(searchCondition).sort(condition.sortBy, orderBy)
        cursor = cursor.skip(condition.offset).limit(condition.take)
        
        result = list(cursor)
        return genericSerialMapper(result) if result else None
    
    def getCount(self, condition: Dict[str, Any]) -> int:
        """ Get count of documents meeting condition """
        return self._collection.count_documents(condition)

    
    def _getOrderFromString(self, orderType: str) -> int:
        """ Returns item oderder option as int """
        if not self._isValidOrder(orderType):
            raise InvalidOrderException()
        return 1 if orderType == "ASC" else -1
        
    def _isValidOrder(self, orderType: str) -> bool:
        """ Validate if given order type matches enum value """
        return any(orderType == status.value for status in SortedBy)
    
    def __enter__(self):
        return self
    
    def __exit__(self, ex_type, exc_value, traceback):
        pass

    
    
