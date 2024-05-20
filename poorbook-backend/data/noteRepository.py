from .repository import Repository

class NoteRepository(Repository):
    """ Note-specific repository """
    
    def __init__(self) -> None:
        self.COLLECTION_NAME = "poor-notes"
        super().__init__(self.COLLECTION_NAME)
    