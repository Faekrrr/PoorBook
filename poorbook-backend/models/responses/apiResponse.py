import sys
sys.path.append('.')
from pydantic import BaseModel
from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from common.logger import InternalLogging
from starlette import status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder



class ApiResponse(BaseModel):
    """ API Global response model """
    message: str = 'default'
    statusCode: int = None
    content: dict = {}

    @classmethod
    def createResponse(cls):
        """ Create new response """
        return cls()
    
    def addContent(self, content):
        """ Add content to response"""
        self.content = {"result": content}
        return self
    
    def asSuccess(self, statusCode: int):
        """ Return success message """
        self.message = "success"
        self.statusCode = statusCode
        return JSONResponse(
            status_code= self.statusCode,
            content=jsonable_encoder(self.model_dump())
        )
    
    def asError(self, exception: Exception, statusCode: int = None):
        """ Return error message """
        self.message = "failed"
        self.statusCode = statusCode if statusCode is not None else self._getStatusCode(exception)
        self.content = str(exception)

        return JSONResponse(
            status_code=self.statusCode,
            content=self.model_dump()
        )

    def _getStatusCode(self, exception: Exception) -> int:
        """ Get status code based on exception type """
        logger = InternalLogging()

        if isinstance(exception, RequestValidationError):
            return status.HTTP_422_UNPROCESSABLE_ENTITY
        
        if isinstance(exception, HTTPException):
            return exception.status_code
        
        logger.error(f"Internal Server Error: [EX]: {exception}")
        return status.HTTP_500_INTERNAL_SERVER_ERROR
        