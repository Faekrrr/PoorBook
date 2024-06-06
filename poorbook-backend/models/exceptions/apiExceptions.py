from fastapi import status

class CustomApiException(Exception):
    """ Custom exception type for poor-backend"""
    def __init__(self, message: str = "Backend error", name: str = "PoorBackend", status: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
        self._message = message
        self._name = name
        self._status = status
        super().__init__(self._message, self._name)
        
    @property
    def status(self):
        return self._status
    
    
class InvalidApiKeyException(CustomApiException):
    """ Error validating given API Key """
    def __init__(self, message: str = "Error validating given API key."):
        super().__init__(status=status.HTTP_401_UNAUTHORIZED, message=message, name="InvalidApiKeyException")
    

class ItemNotFoundException(CustomApiException):
    """ Requested item/s cannot be found """
    def __init__(self, message: str = "Item hasnt been found."):
        super().__init__(status=status.HTTP_404_NOT_FOUND, message=message, name="ItemNotFoundException")

class MissingApiKeyException(CustomApiException):
    """ Backend didnt receive API key in header """
    def __init__(self, message: str = "API key not in header"):
        super().__init__(status=status.HTTP_403_FORBIDDEN, message=message, name="MissingApiKeyException")

class StatusAlreadySetException(CustomApiException):
    """ Given status has been already set for requested task """
    def __init__(self, message: str = "Given status already set "):
        super().__init__(status=status.HTTP_409_CONFLICT, message=message, name="StatusAlreadySetException")

class InvalidIdFormatException(CustomApiException):
    """ Given item ID is not valid ObjectId format """
    def __init__(self, message: str = " Invalid Id 0 should be ObjectId "):
        super().__init__(status=status.HTTP_400_BAD_REQUEST, message=message, name="InvalidIdFormatException")
  
class ItemNotCreatedException(CustomApiException):
    """ Given item hasnt been created due to exception """
    def __init__(self, message: str = "Item hasnt been created"):
        super().__init__(status=status.HTTP_400_BAD_REQUEST, message=message, name="ItemNotCreatedException")      
        

class ItemNotDeletedException(CustomApiException):
    """ Given item hasnt been created due to exception """
    def __init__(self, message: str = "Item hasnt been deleted"):
        super().__init__(status=status.HTTP_400_BAD_REQUEST, message=message, name="ItemNotDeletedException") 
        
class ItemNotUpdatedException(CustomApiException):
    """ Given item hasnt been created due to exception """
    def __init__(self, message: str = "Item hasnt been updated"):
        super().__init__(status=status.HTTP_400_BAD_REQUEST, message=message, name="ItemNotUpdatedException") 