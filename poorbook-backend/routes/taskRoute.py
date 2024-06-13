from fastapi import APIRouter, Depends, Query, status
from models.responses.apiResponse import ApiResponse
from models.entities.task import Task, UpdateTaskStatus, CreateTaskModel
from models.requests.tasksModels import TaskByConditionModel
from models.app.conditionModel import ConditionModel
from services.taskService import TaskService
from models.exceptions.apiExceptions import ItemNotCreatedException, ItemNotDeletedException, ItemNotUpdatedException
from data.taskRepository import TaskRepository
from typing import Optional

tasksRouter = APIRouter()

@tasksRouter.post("/tasks", response_model=ApiResponse,
                  summary="Create new task.",
                  description="Create new tasks by passing task model.",
                  tags=["Tasks"])
async def insertTask(newTask: CreateTaskModel, repository: TaskRepository = Depends()):
    """ Insert new task """
    result = repository.insert(Task(
        taskTitle=newTask.taskTitle,
        taskDesc=newTask.taskDesc,
        taskDonedate=newTask.taskDonedate
    ))

    if not result:
        raise ItemNotCreatedException("Task hasnt been created.")
   
    return ApiResponse.createResponse().addContent({"id": f'{result}'}).asSuccess(status.HTTP_201_CREATED)

    
@tasksRouter.get("/tasks", response_model= ApiResponse,
                 summary="Get tasks.",
                 description="Get top 10 tasks that are not DONE.",
                 tags=["Tasks"])
async def getTasks(offset: int = Query(0, description="How much to skip"),
                   take: int = Query(10, description="How much to take"),
                   order: str = Query("ASC", description="How to order"),
                   sortBy: str = Query("taskCreated", description="Which property to sort by"),
                   repository: TaskRepository = Depends()):
    """ Get tasks """
    result = repository.getSorted(ConditionModel(
        take=take,
        offset=offset,
        filterBy={"taskStatus": {"$ne": "DONE"}},
        sortOrder=order,
        sortBy=sortBy
    ))
    
    return ApiResponse.createResponse().addContent(result).asSuccess(status.HTTP_200_OK)
    
    
@tasksRouter.post("/tasks/search", response_model= ApiResponse, 
                  summary="Get tasks by criteria.", 
                  description="Retrieve tasks based on specific filtering and sorting criteria.",
                  tags=["Tasks"])
async def getTasksByCondition(condition: Optional[TaskByConditionModel],
                              offset: int = Query(0, description="How much to skip"),
                              take: int = Query(10, description="How much to take"),
                              order: str = Query("ASC", description="How to order"),
                              sortBy: str = Query("taskCreated", description="Which property to sort by"),
                              repository: TaskRepository = Depends()):
    """ Get tasks by criteria """
    result = repository.getSorted(ConditionModel(
        take=take,
        offset=offset,
        condition=condition.dict(),
        sortOrder=order,
        sortBy=sortBy   
    ))
        
    return ApiResponse.createResponse().addContent(result).asSuccess(status.HTTP_200_OK)
    

@tasksRouter.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT,
                    summary="Delete task by Id.",
                    description="Delete task providing task Id.",
                    tags=["Tasks"])
async def deleteTask(id: str, repository: TaskRepository = Depends()):
    """ Delete task by Id """
    result = repository.delete(id)
    if not result:
        raise ItemNotDeletedException("Task hasnt been deleted")
    
    
@tasksRouter.put("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT,
                 summary="Update task by Id.",
                 description="Update task providing Id and new task body.",
                 tags=["Tasks"])
async def updateTask(id: str, changes: Task, repository: TaskRepository = Depends()):
    """ Update task by Id """
    result = repository.update(id, changes)

    if not result:
        raise ItemNotUpdatedException("Tasks hasnt been updated")

    
@tasksRouter.put("/tasks/status/{id}", status_code=status.HTTP_204_NO_CONTENT,
                 summary="Update task's status.",
                 description="Update tasks of given Id by new status. Not accepting the same status as current one.",
                 tags=["Tasks"])
async def updateStatusOfTask(id: str, newStatus: UpdateTaskStatus, repository: TaskRepository = Depends()):
    """ Update given task's status """
    result = repository.changeStatus(id, newStatus.taskStatus)

    if not result:
        raise ItemNotUpdatedException("Tasks hasnt been updated")
    

@tasksRouter.get("/tasks/progress/all", response_model= ApiResponse, 
                  summary="Get quantity of all today's tasks.", 
                  description="Retrieve quantity of tasks which donedate is equal or greater than today.",
                  tags=["Tasks/Progress"])
def getAllTodaysTasks(service: TaskService = Depends()):
    """ Get quantity of all tasks => today's date. """
    result = service.getTasksQuantityByDate()
    return ApiResponse.createResponse().addContent(result).asSuccess(status.HTTP_200_OK)
    

@tasksRouter.get("/tasks/progress/percentage", response_model= ApiResponse, 
                  summary="Get procentage of DONE task", 
                  description="Retrieve procentage of DONE tasks which donedate is equal or greater than today.",
                  tags=["Tasks/Progress"])
def getDoneTasksPercentage(service: TaskService = Depends()):
    """ Get done tasks procentage agains all tasks => today's date. """
    result = service.getDoneTasksPercentageByDate()
    return ApiResponse.createResponse().addContent(result).asSuccess(status.HTTP_200_OK)

@tasksRouter.get("/tasks/progress/done", response_model= ApiResponse, 
                  summary="Get quantity of DONE tasks", 
                  description="Retrieve quantity of DONE tasks which donedate is equal or greater than today.",
                  tags=["Tasks/Progress"])
def getDoneTasksQuantity(service: TaskService = Depends()):
    """ Get done tasks quantity => today's date. """
    result = service.getDoneTasksQuantityByDate()
    return ApiResponse.createResponse().addContent(result).asSuccess(status.HTTP_200_OK)
    
