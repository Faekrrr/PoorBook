from pydantic import BaseModel, validator
from ..enums.taskStatus import TaskStatus
from datetime import datetime


class Task(BaseModel):
    """ Task entity model """
    taskTitle: str
    taskDesc: str
    taskStatus: str
    taskCreated: datetime
    taskDonedate: datetime

    @validator("taskStatus")
    def validateExperienceLevel(cls, value):
        """ Validate experience level agains enum """
        return cls._validateValue(value, TaskStatus)

    @validator("taskTitle")
    def validateTaskTitle(cls, value):
        """ Validate task name value"""
        MAX_STRING_LEN = 255
        if len(value) > MAX_STRING_LEN:
            raise ValueError("Task name too long")
        return value

    @classmethod
    def _validateValue(cls, value, enumType):
        """ Validate given value against given enum"""
        validValues = [member.value for member in enumType]
        if value.upper() not in validValues:
            raise ValueError(f"Invalid value, should be one of: {validValues}")
        return value

