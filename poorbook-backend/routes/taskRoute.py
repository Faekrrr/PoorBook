from fastapi import APIRouter, Depends, Query, status
from models.responses.apiResponse import ApiResponse
from models.entities.task import Task, UpdateTaskStatus
from models.exceptions.apiExceptions import ItemNotFoundException, ItemNotCreatedException, ItemNotDeletedException, ItemNotUpdatedException
from data.taskRepository import TaskRepository
from typing import Optional, Dict, Any

tasksRouter = APIRouter()


@tasksRouter.post("/tasks", response_model=ApiResponse)
async def insertTask(newTask: Task, repository: TaskRepository = Depends()):
    """ Insert new task """
    result = repository.insert(newTask)

    if not result:
        raise ItemNotCreatedException("Task hasnt been created.")
   
    return ApiResponse.createResponse().asSuccess(status.HTTP_201_CREATED)

    
@tasksRouter.get("/tasks", response_model= ApiResponse)
async def getTasks(offset: int = Query(0, description="How much to skip"),
                   take: int = Query(10, description="How much to take"),
                   repository: TaskRepository = Depends()):
    """ Get tasks """
    result = repository.get(offset, take)

    if not result:
        raise ItemNotFoundException("No tasks found.")
    
    return ApiResponse.createResponse().addContent(result).asSuccess(status.HTTP_200_OK)
    
    
@tasksRouter.post("/tasks/condition", response_model= ApiResponse)
async def getTasksByCondition(condition: Optional[Dict[str, Any]],
                              offset: int = Query(0, description="How much to skip"),
                              take: int = Query(10, description="How much to take"),
                              repository: TaskRepository = Depends()):
    """ Get tasks by criteria """
    result = repository.get(offset, take, condition)

    if not result:
        raise ItemNotFoundException("No tasks found.")
        
    return ApiResponse.createResponse().addContent(result).asSuccess(status.HTTP_200_OK)
    

@tasksRouter.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def deleteTask(id: str, repository: TaskRepository = Depends()):
    """ Delete task by Id """
    result = repository.delete(id)
    if not result:
        raise ItemNotDeletedException("Task hasnt been deleted")
    
    
@tasksRouter.put("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def updateTask(id: str, changes: Task, repository: TaskRepository = Depends()):
    """ Update task by Id """
    result = repository.update(id, changes)

    if not result:
        raise ItemNotUpdatedException("Tasks hasnt been updated")

    
@tasksRouter.put("/tasks/status/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def updateStatusOfTask(id: str, newStatus: UpdateTaskStatus, repository: TaskRepository = Depends()):
    """ Update given task's status """
    result = repository.changeStatus(id, newStatus.taskStatus)

    if not result:
        raise ItemNotUpdatedException("Tasks hasnt been updated")
    
