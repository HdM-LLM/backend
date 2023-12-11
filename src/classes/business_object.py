from abc import ABC
from uuid import UUID, uuid4
from datetime import datetime


class BusinessObject(ABC):

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

