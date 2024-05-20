from fastapi import APIRouter, Depends, HTTPException, Query, status
from models.responses.apiResponse import ApiResponse
from models.entities.task import Task, UpdateTaskStatus
from models.exceptions.statusAlreadySetException import StatusAlreadySetException
from data.taskRepository import TaskRepository

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
        
        return ApiResponse.createResponse().asSuccess(status.HTTP_201_CREATED)
        
    except Exception as ex:
        return ApiResponse.createResponse().asError(ex)
    
    
@tasksRouter.get("/tasks", response_model= ApiResponse)
async def getTasks(offset: int = Query(0, description="How much to skip"),
                   take: int = Query(10, description="How much to take"),
                   repository: TaskRepository = Depends()):
    """ Get tasks """
    try:
        result = repository.get({}, offset, take)

        if result is None or len(result) == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    
        return ApiResponse.createResponse().addContent(result).asSuccess(status.HTTP_200_OK)
    
    except Exception as ex:
        return ApiResponse.createResponse().asError(ex)
    

@tasksRouter.delete("/tasks/{id}")
async def deleteTask(id: str, repository: TaskRepository = Depends()):
    """ Delete task by Id """
    try:
        result = repository.delete(id)

        if not result:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tasks hasnt been deleted")
    
    except Exception as ex:
        return ApiResponse.createResponse().asError(ex)
    
@tasksRouter.put("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def updateTask(id: str, changes: Task, repository: TaskRepository = Depends()):
    """ Update task by Id """
    try:
        result = repository.update(id, changes)

        if not result:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tasks hasnt been updated")
        
    except Exception as ex:
        return ApiResponse.createResponse().asError(ex)
    

@tasksRouter.put("/tasks/status/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def updateStatusOfTask(id: str, newStatus: UpdateTaskStatus, repository: TaskRepository = Depends()):
    """ Update given task's status """
    try:
        result = repository.changeStatus(id, newStatus.taskStatus)

        if not result:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tasks hasnt been updated")

    except StatusAlreadySetException as ex:
        return ApiResponse.createResponse().asError(ex, status.HTTP_400_BAD_REQUEST)

    except Exception as ex:
        return ApiResponse.createResponse().asError(ex)