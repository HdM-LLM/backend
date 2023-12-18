from abc import ABC, abstractmethod
import mysql.connector


class MySQLMapper(ABC):

    def __init__(self):
        self._connection = None

    def __enter__(self):
        self._connection = mysql.connector.connect(
            user='root',
            password='password',
            host='127.0.0.1',
            database='skillsync',
            port='3307',
        )

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._connection.close()

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_by_id(self, id):
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