import sys
sys.path.append('.')

from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette import status
from models.responses.apiResponse import ApiResponse
from models.exceptions.invalidApiKeyException import InvalidApiKeyException
from models.exceptions.missingApiKeyException import MissingApiKeyException


def handleValidationError(request: Request, exception: RequestValidationError):
    """ Handle RequestValidationError from pydantic """
    response = ApiResponse.createErrorResponse(exception)
    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=response.model_dump())

def handleApiKeyValidation(request: Request, exc: InvalidApiKeyException):
    """ Handle InvalidApiKey exception """
    statusCode = status.HTTP_401_UNAUTHORIZED
    response = ApiResponse.createCustomErrorRespomse(statusCode=statusCode, exception=exc)
    return JSONResponse(status_code=statusCode, content=response.model_dump())

def handleMissingApiKeyValidation(request: Request, exc: MissingApiKeyException):
    """ Handle MissinApiKey exception """
    statusCode = status.HTTP_403_FORBIDDEN
    response = ApiResponse.createCustomErrorRespomse(statusCode=statusCode, exception=exc)
    return JSONResponse(status_code=statusCode, content=response.model_dump())