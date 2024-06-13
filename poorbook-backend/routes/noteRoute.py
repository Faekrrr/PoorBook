from fastapi import APIRouter, Depends, Query, status
from models.responses.apiResponse import ApiResponse
from models.entities.note import Note, CreateNoteModel
from data.noteRepository import NoteRepository
from models.exceptions.apiExceptions import ItemNotCreatedException, ItemNotDeletedException, ItemNotUpdatedException
from models.app.conditionModel import ConditionModel


noteRouter = APIRouter()

@noteRouter.post("/notes", response_model=ApiResponse,
                summary="Create new note.",
                description="Create a new note using the Note model.",
                tags=["Notes"])
async def insertNote(newNote: CreateNoteModel, repository: NoteRepository = Depends()):
    """ Creates new note in collection """
    result = repository.insert(Note(
        content=newNote.content
    ))

    if not result:
        raise ItemNotCreatedException("Note hasn't been created.")
   
    return ApiResponse.createResponse().asSuccess(status.HTTP_201_CREATED)

@noteRouter.get("/notes", response_model=ApiResponse,
               summary="Get all notes.",
               description="Get all notes with pagination.",
               tags=["Notes"])
def getNotes(offset: int = Query(0, description="How much to skip"),
                take: int = Query(10, description="How much to take"),
                order: str = Query("ASC", description="How to order"),
                repository: NoteRepository = Depends()):
    """ Gets all notes from collection """
    result = repository.getSorted(ConditionModel(
        take=take,
        offset=offset,
        sortOrder=order,
        sortBy="created"
    ))
    
    return ApiResponse.createResponse().addContent(result).asSuccess(status.HTTP_200_OK)


@noteRouter.delete("/notes/{id}", status_code=status.HTTP_204_NO_CONTENT,
                  summary="Delete note by Id.",
                  description="Delete note with provided Id.",
                  tags=["Notes"])
def deleteNote(id: str, repository: NoteRepository = Depends()):
    """ Deletes note by Id """
    result = repository.delete(id)
    if not result:
        raise ItemNotDeletedException("Note hasnt been deleted")
    
@noteRouter.put("/notes/{id}",
                summary="Update note by Id.",
                description="Update note of provided Id with provided content.",
                status_code=status.HTTP_204_NO_CONTENT,
                tags=["Notes"])
async def updateNote(id: str, changes: Note, repository: NoteRepository = Depends()):
    """ Update note by Id """
    result = repository.update(id, changes)

    if not result:
        raise ItemNotUpdatedException("Note hasnt been updated")