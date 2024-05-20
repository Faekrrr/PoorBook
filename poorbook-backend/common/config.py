import os

class Config():
    """ App cofnig """

    def __init__(self) -> None:
        
        #mongo host name 
        self.MONGO_HOST = os.environ.get("MONGO_HOST", "")
        self.MONGO_DATABASE = os.environ.get("MONGO_DATABASE", "")
        self.ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "")
        self.MONGO_USER = os.environ.get("MONGO_USER", "")
        self.MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD", "")

        #api key
        self.API_KEY = os.environ.get("API_KEY", "")

