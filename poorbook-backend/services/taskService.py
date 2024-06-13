from data.taskRepository import TaskRepository
from datetime import datetime

class TaskService():
    """ Business logic related to managing Tasks objects """
    def __init__(self) -> None:
        self._repository = TaskRepository()
        
    def getTasksQuantityByDate(self, date: datetime = datetime.now()) -> int:
        """ Get quantity of all tasks equals or greater than given date. """
        condition = {
            "taskDonedate": {
                "$gte": date
            }
        }
        return self._repository.getCount(condition)
        
    def getDoneTasksQuantityByDate(self, date: datetime = datetime.now()) -> int:
        """ Get quantity of all tasks that are done and equals or greater than given date. """
        condition = {
            "taskDonedate": {
                "$gte": date
            },
            "taskStatus": 'DONE'
        }
        return self._repository.getCount(condition)
    
    def getDoneTaskPercentageByDate(self, date: datetime = datetime.now()) -> int:
        """ Get percentage of done tasks equals or greater than given date. """
        allTasks = self.getTasksQuantityByDate(date)
        doneTasks = self.getDoneTasksQuantityByDate(date)
              
        return 0 if allTasks == 0 else round((doneTasks/allTasks)*100)