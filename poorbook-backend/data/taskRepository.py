from .repository import Repository
from bson import ObjectId
from mappers.genericMapper import genericMapper
from models.exceptions.statusAlreadySetException import StatusAlreadySetException

class TaskRepository(Repository):
    """ Task-specific repository """
    def __init__(self) -> None:
        self.COLLECTION_NAME = "poor-tasks"
        super().__init__(self.COLLECTION_NAME)

    def changeStatus(self, taskId: str, status) -> bool:
        """ Changes Task's status"""
        currentStatus = self.getCurrentStatus(taskId)

        if(currentStatus == status.value):
            raise StatusAlreadySetException()
        
        result = self._collection.update_one({"_id": ObjectId(taskId)}, {"$set": {'taskStatus': status.value}})
        return result.modified_count > 0

    def getCurrentStatus(self, taskId: str) -> str:
        """ Checks current task's status """
        result = self._collection.find_one({"_id": ObjectId(taskId)})
        task = genericMapper(result) if result else None
        return task["taskStatus"]