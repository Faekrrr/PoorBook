from data.connection import Connection
from mappers.genericMapper import genericMapper, genericSerialMapper
from bson import ObjectId
from typing import Optional, Any, Dict


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
    
    def get(self, condition: Optional[Dict[str, Any]], offset: int, take: int):
        """ Get items by given criteria """
        if condition is None or condition == {}:
            cursor = self._collection.find()
        else:
            cursor = self._collection.find(condition)

        cursor = cursor.skip(offset).limit(take)
        result = list(cursor)
        return genericSerialMapper(result) if result else None

    
    def __enter__(self):
        return self
    
    def __exit__(self, ex_type, exc_value, traceback):
        pass

    
    
