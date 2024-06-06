from common.config import Config
from fastapi.security.api_key import APIKeyHeader
from fastapi import Security
from models.exceptions.apiExceptions import MissingApiKeyException, InvalidApiKeyException

class Authenticator():
    """ Handle API Key authentication """

    def __init__(self) -> None:
        self._config = Config()
        self.API_KEY = self._config.API_KEY

    def validateApiKey(self, keyToValidate: str = Security(APIKeyHeader(name="X-API-Key", auto_error=False))) -> str:
        """ Validates given API key """
        if keyToValidate is None:
            raise MissingApiKeyException()
        
        if keyToValidate != self.API_KEY:
            raise InvalidApiKeyException()
        return keyToValidate
