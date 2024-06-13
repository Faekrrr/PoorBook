from pydantic import BaseModel, field_validator
from models.enums.taskStatus import TaskStatus
from datetime import datetime


class TaskModel(BaseModel):
    """ Basic task model. """
    taskTitle: str
    taskDesc: str
    taskDonedate: datetime
    
    @field_validator("taskTitle")
    def validateTaskTitle(cls, value):
        """ Validate task name value. """
        MAX_STRING_LEN = 255
        if len(value) > MAX_STRING_LEN:
            raise ValueError("Task name too long")
        return value
    
class CreateTaskModel(TaskModel):
    """ Request model to create new Task.  """
    pass

class Task(TaskModel):
    """ Task entity model """
    taskStatus: str = 'TODO'
    taskCreated: datetime = datetime.now()

    @field_validator("taskStatus")
    def validateExperienceLevel(cls, value):
        """ Validate experience level agains enum """
        return cls._validateValue(value, TaskStatus)

    @classmethod
    def _validateValue(cls, value, enumType):
        """ Validate given value against given enum"""
        validValues = [member.value for member in enumType]
        if value.upper() not in validValues:
            raise ValueError(f"Invalid value, should be one of: {validValues}")
        return value

class UpdateTaskStatus(BaseModel):
    taskStatus: str

    @field_validator("taskStatus")
    def validateTaskStatus(cls, value):
        """ Validate experience level agains enum """
        return cls._validateValue(value, TaskStatus)
    
    @classmethod
    def _validateValue(cls, value, enumType):
        """ Validate given value against given enum"""
        validValues = [member.value for member in enumType]
        if value.upper() not in validValues:
            raise ValueError(f"Invalid value, should be one of: {validValues}")
        return value