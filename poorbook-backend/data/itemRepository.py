from data.repository import Repository

class ItemRepository(Repository):
    """ Item-specific repository """
    def __init__(self) -> None:
        self.COLLECTION_NAME = "poor-items"
        super().__init__(self.COLLECTION_NAME)