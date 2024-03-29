from abc import ABC
from classes.business_object import BusinessObject


class User(BusinessObject, ABC):
    """Class which represents a User inside the system

    Args:
        BusinessObject (BusinessObject): Inherits BusinessObject class
        ABC (ABC): Inherits ABC class
    """

    def __init__(
            self,
            first_name: str,
            last_name: str,
    ) -> None:
        """Creates a instance of a User

        Args:
            first_name (str): First name of a user
            last_name (str): Last name of a user
        """
        super().__init__()
        self._first_name = first_name
        self._last_name = last_name

    def get_first_name(self) -> str:
        return self._first_name

    def set_first_name(self, first_name) -> None:
        self._first_name = first_name

    def get_last_name(self) -> str:
        return self._last_name

    def set_last_name(self, last_name) -> None:
        self._last_name = last_name
