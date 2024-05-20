from fastapi import APIRouter, Depends, HTTPException, Query, status
from models.responses.apiResponse import ApiResponse
from models.entities.task import Task
from models.enums.taskStatus import TaskStatus
from models.exceptions.statusAlreadySetException import StatusAlreadySetException
from data.taskRepository import TaskRepository
from typing import Optional, Dict, Any

tasksRouter = APIRouter()


@tasksRouter.post("/tasks", response_model=ApiResponse)
async def insertTask(newTask: Task, repository: TaskRepository = Depends()):
    """ Insert new task """
    try:
        if newTask is None or not isinstance(newTask, Task):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid input data.")
        
        result = repository.insert(newTask)

        if not result:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Operation failed")
        
        return ApiResponse.createSuccessResponse(statusCode=status.HTTP_201_CREATED, content={})
        
    except Exception as ex:
        return ApiResponse.createErrorResponse(exception=ex)
    
    
@tasksRouter.get("/tasks", response_model= ApiResponse)
async def getTasks(offset: int = Query(0, description="How much to skip"),
                   take: int = Query(10, description="How much to take"),
                   repository: TaskRepository = Depends()):
    """ Get tasks by condition """
    try:
        result = repository.get({}, offset, take)

        if result is None or len(result) == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
        
        return ApiResponse.createSuccessResponse(statusCode=status.HTTP_200_OK, content={"result": result})
    
    except Exception as ex:

        return ApiResponse.createErrorResponse(exception=ex)
    

@tasksRouter.delete("/tasks/{id}")
async def deleteTask(id: str, repository: TaskRepository = Depends()):
    """ Delete task by Id """
    try:
        result = repository.delete(id)

        if not result:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tasks hasnt been deleted")
        
        return ApiResponse(status=status.HTTP_204_NO_CONTENT, content={})
    
    except Exception as ex:
        return ApiResponse.createErrorResponse(exception=ex)
    
@tasksRouter.put("/tasks/{id}")
async def updateTask(id: str, changes: Task, repository: TaskRepository = Depends()):
    """ Update task by Id """
    try:
        result = repository.update(id, changes)

        if not result:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tasks hasnt been updated")
        
        return ApiResponse(status=status.HTTP_204_NO_CONTENT, content={})

    except Exception as ex:
        return ApiResponse.createErrorResponse(exception=ex)
    
@tasksRouter.put("/tasks/{id}")
async def updateStatusOfTask(id: str, newStatus: TaskStatus, repository: TaskRepository = Depends()):
    """ Update given task's status """
    try:
        result = repository.changeStatus(id, newStatus)

        if not result:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tasks hasnt been updated")
        
        return ApiResponse.createSuccessResponse(statusCode=status.HTTP_204_NO_CONTENT)

    except StatusAlreadySetException as ex:
        return ApiResponse.createCustomErrorRespomse(statusCode=status.HTTP_400_BAD_REQUEST, exception=ex)

    except Exception as ex:
        return ApiResponse.createErrorResponse(exception=ex)