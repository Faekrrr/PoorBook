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
        self.ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(',')
        self.ALLOWED_METHODS = os.environ.get("ALLOWED_METHODS", "").split(',')
        self.ALLOWED_HEADERS = os.environ.get("ALLOWED_HEADERS", "").split(',')

        #api key
        self.API_KEY = os.environ.get("API_KEY", "")

