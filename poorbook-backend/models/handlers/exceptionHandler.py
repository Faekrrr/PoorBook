import sys
sys.path.append('.')

from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from starlette import status
from models.responses.apiResponse import ApiResponse
from models.exceptions.apiExceptions import CustomApiException


def handleValidationError(request: Request, exception: RequestValidationError):
    """ Handle RequestValidationError from pydantic """
    return ApiResponse.createResponse().asError(exception, status.HTTP_422_UNPROCESSABLE_ENTITY)

def handleCustomApiExceptions(requst: Request, exception: CustomApiException):
    """ Handle custom API Exceptions """
    return ApiResponse.createResponse().asError(exception, exception.status)

def handleRegularException(request: Request, exception: Exception):
    """ Handle all unhandled exceptions """
    return ApiResponse.createResponse().asError(exception, status.HTTP_500_INTERNAL_SERVER_ERROR)
