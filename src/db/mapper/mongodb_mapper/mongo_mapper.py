from abc import ABC, abstractmethod
import pymongo
from gridfs import GridFS


class MongoMapper(ABC):
    """Abstract class which implements all necessary properties to use the mongoDB

    Args:
        ABC (ABC): Inherits ABC class to turn the class into a abstract class
    """

    def __init__(self, collection: str):
        self._client = None
        self._database = None
        self._fs = None
        self._collection = None
        self._collection_name = collection

    def __enter__(self):
        """Sets all properties of the mongoDB when using the context manager
        """
        self._client = pymongo.MongoClient(
            'mongodb://root:password@localhost:27017/')
        self._database = self._client['skillsync']
        self._fs = GridFS(self._database)
        self._collection = self._database[self._collection_name]
        return self

    def __exit__(self):
        """Closes the connection of the database
        """
        if self._client is not None:
            self._client.close()

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_by_id(self, id, secondary_id=None):
        pass

    @abstractmethod
    def insert(self, object):
        pass

    @abstractmethod
    def update(self, object):
        pass

    @abstractmethod
    def delete_by_id(self, id):
        pass

    def get_client(self):
        return self._client

    def get_database(self):
        return self._database

    def get_fs(self):
        return self._fs

    def get_collection(self):
        return self._collection
