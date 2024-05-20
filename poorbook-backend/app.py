from fastapi import FastAPI, Depends
from common.config import Config
from models.handlers.exceptionHandler import handleValidationError, handleApiKeyValidation, handleMissingApiKeyValidation
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from models.exceptions.invalidApiKeyException import InvalidApiKeyException
from models.exceptions.missingApiKeyException import MissingApiKeyException
from common.authenticator import Authenticator
from routes.eventRoute import eventRouter
from routes.taskRoute import tasksRouter
import uvicorn

#get authenticator
auth = Authenticator()

#create app
app = FastAPI(dependencies=[Depends(auth.validateApiKey)])

#configure CORS
config = Config()

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"]
)

#add exepcetion handling
app.add_exception_handler(RequestValidationError, handleValidationError)
app.add_exception_handler(MissingApiKeyException, handleMissingApiKeyValidation)
app.add_exception_handler(InvalidApiKeyException, handleApiKeyValidation)

#add routes
API_PREFIX = "/api/v1"
app.include_router(tasksRouter, prefix=API_PREFIX)
app.include_router(eventRouter, prefix=API_PREFIX)

#run uvicorn
if __name__ == '__main__':
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)