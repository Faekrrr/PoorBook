import sys
sys.path.append('.')

from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from starlette import status
from models.responses.apiResponse import ApiResponse
from models.exceptions.invalidApiKeyException import InvalidApiKeyException
from models.exceptions.missingApiKeyException import MissingApiKeyException


def handleValidationError(request: Request, exception: RequestValidationError):
    """ Handle RequestValidationError from pydantic """
    return ApiResponse.createResponse().asError(exception, status.HTTP_422_UNPROCESSABLE_ENTITY)


def handleApiKeyValidation(request: Request, exception: InvalidApiKeyException):
    """ Handle InvalidApiKey exception """
    return ApiResponse.createResponse().asError(exception, status.HTTP_401_UNAUTHORIZED)


def handleMissingApiKeyValidation(request: Request, exception: MissingApiKeyException):
    """ Handle MissinApiKey exception """
    return ApiResponse.createResponse().asError(exception, status.HTTP_403_FORBIDDEN)