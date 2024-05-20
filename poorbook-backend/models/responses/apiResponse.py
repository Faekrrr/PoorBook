import sys
sys.path.append('.')
from pydantic import BaseModel
from typing import Optional
from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from common.logger import InternalLogging
from starlette import status
from starlette.responses import Response
from fastapi.responses import JSONResponse



class ApiResponse(BaseModel):
    """ Api endpoint response model """
    message: str
    status: Optional[int] = None
    content: dict = {}

    @classmethod
    def createErrorResponse(cls, exception: Exception):
        """ Create error response """

        response = cls(message="failed")
        logger = InternalLogging()

        if isinstance(exception, HTTPException):
            response.status = exception.status_code

        elif isinstance(exception, RequestValidationError):
            response.status = status.HTTP_422_UNPROCESSABLE_ENTITY
           
        else:
            response.status = status.HTTP_500_INTERNAL_SERVER_ERROR
            logger.error(f"Internal Server Error: [EX]: {exception}")

        response.content = {"details": str(exception)}
        return response
    
    @classmethod
    def createCustomErrorRespomse(cls, statusCode: int, exception: Exception):
        """ Create error response with custom status code """
        return cls(
            message="failed",
            status=statusCode,
            content={"details": str(exception)}
        )
    
    @classmethod
    def createSuccessResponse(cls, statusCode: int , content: dict = {"result": "no content"}):
        """ Create success response """
        return cls(
            message="success",
            status=statusCode,
            content=content
        )
    
