import os

class Config():
    """ App cofnig """

    def __init__(self) -> None:
        
        #mongo host name 
        self.MONGO_HOST = os.environ.get("MONGO_HOST", "")
        self.MONGO_DATABASE = os.environ.get("MONGO_DATABASE", "")
        self.MONGO_USER = os.environ.get("MONGO_USER", "")
        self.MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD", "")

        #CORS
        self.ALLOWED_HOSTS = self._loadValueAsList("ALLOWED_HOSTS")
        self.ALLOWED_METHODS = self._loadValueAsList("ALLOWED_METHODS")
        self.ALLOWED_HEADERS = self._loadValueAsList("ALLOWED_HEADERS")

        #api key
        #DEV:
        self.API_KEY = os.environ.get("API_KEY", "ioxnsaunxa")
        #PROD:
        #self.API_KEY = os.environ.get("API_KEY", "")

    def _loadValueAsList(self, envName: str, default = "*"):
        """ Load values from env as a list """
        envToProcess = os.getenv(envName, default)
        return [env.strip() for env in envToProcess.split(',') if env.strip()]
            

