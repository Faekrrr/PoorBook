from data.repository import Repository
from models.app.conditionModel import ConditionModel
from models.requests.eventsModels import EventsByRangeModel

class EventRepository(Repository):
    """ Event-specific repository. """

    def __init__(self) -> None:
        self.COLLECTION_NAME = "poor-events"
        super().__init__(self.COLLECTION_NAME)

    def getMonth(self, conditionParameters: ConditionModel, month: str, year: int):
        """ Get event from specific month. """
        conditionParameters.condition = {
            "eventMonth": month,
            "eventYear": year
        }
        return self.getSorted(conditionParameters)
    
    def getRange(self, conditionParameters: ConditionModel, range: EventsByRangeModel):
        """ Get events based on data range. """
        conditionParameters.condition = {
            "eventDate": {
                "$gte": range.dateFrom,
                "$lt": range.dateTo
            }
        }
        return self.getSorted(conditionParameters)
               

    