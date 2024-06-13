from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TaskByConditionModel(BaseModel):
    """ Request model to get tasks passing conditions. """
    taskTitle: Optional[str] = None
    taskDesc: Optional[str] = None
    taskDonedate: Optional[datetime] = None
    taskStatus: Optional[str] = None
    taskCreated: Optional[datetime] = None