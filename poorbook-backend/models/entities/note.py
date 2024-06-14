from pydantic import BaseModel, Field
from datetime import datetime



class NoteModel(BaseModel):
    """ Basic note model. """
    content: str
    
class CreateNoteModel(NoteModel):
    """ Request model to create new Note. """
    pass

class Note(NoteModel):
    """ Note object Model. """
    created: datetime = Field(default_factory=datetime.now)
    
        
    
    
    

