from abc import ABC
from uuid import UUID, uuid4
from datetime import datetime


class BusinessObject(ABC):
    """Abstract class which implements the id and creation date for all other classes

    Args:
        ABC (ABC): Inherits ABC class to turn the class into a abstract class
    """

    def __init__(self) -> None:
        self._id = uuid4()
        self._creation_date = datetime.now()

    def get_id(self) -> UUID:
        return self._id

    def set_id(self, uuid) -> None:
        self._id = uuid

    def get_creation_date(self) -> datetime:
        return self._creation_date

    def set_creation_date(self, creation_date: datetime) -> None:
        self._creation_date = creation_date

