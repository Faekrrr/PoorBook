from pymongo import MongoClient
from common.config import Config


class Connection():
    """ Create connection to mongo db"""
    #add auth
    def __init__(self) -> None:
        self._config = Config()
        self._mongoClient = MongoClient(self._config.MONGO_HOST, 27017)
        self._database = self._mongoClient[self._config.MONGO_DATABASE]

    @property
    def database(self):
        return self._database
