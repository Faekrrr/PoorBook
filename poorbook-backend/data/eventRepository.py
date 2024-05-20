from .repository import Repository
from datetime import datetime

class EventRepository(Repository):
    """ Event-specific repository """

    def __init__(self) -> None:
        self.COLLECTION_NAME = "poor-events"
        super().__init__(self.COLLECTION_NAME)


    