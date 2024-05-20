import sys
sys.path.append('.')

from enum import Enum

class TaskStatus(Enum):
    """Available task statusys """
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    BLOCKED = "BLOCKED"
    TODO = "TODO"