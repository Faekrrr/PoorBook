from fastapi import FastAPI, Depends
from common.config import Config
from models.handlers.exceptionHandler import handleValidationError, handleCustomApiExceptions, handleRegularException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from common.authenticator import Authenticator
from routes.eventRoute import eventRouter
from routes.taskRoute import tasksRouter
from routes.noteRoute import noteRouter
from models.exceptions.apiExceptions import CustomApiException
import uvicorn

#get authenticator
auth = Authenticator()

#create app
app = FastAPI(dependencies=[Depends(auth.validateApiKey)],
              title="Poor-backend",
              version="0.5.1")

#configure CORS
config = Config()

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=config.ALLOWED_METHODS,
    allow_headers=config.ALLOWED_HEADERS
)

#add exepcetion handling
app.add_exception_handler(RequestValidationError, handleValidationError)
app.add_exception_handler(CustomApiException, handleCustomApiExceptions)
app.add_exception_handler(Exception, handleRegularException)

#add routes
API_PREFIX = "/api/v1"
app.include_router(tasksRouter, prefix=API_PREFIX)
app.include_router(eventRouter, prefix=API_PREFIX)
app.include_router(noteRouter, prefix=API_PREFIX)

#run uvicorn
if __name__ == '__main__':
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)