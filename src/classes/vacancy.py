from typing import List
from classes.business_object import BusinessObject


class Vacancy(BusinessObject):

    def __init__(
            self,
            name: str,
            department: str,
    ) -> None:
        super().__init__()
        self._name = name
        self._department = department
        self._categories = []

    def get_name(self) -> str:
        return self._name

    def set_name(self, name: str) -> None:
        self._name = name

    def get_department(self) -> str:
        return self._department

    def set_department(self, department: str) -> None:
        self._department = department

    def get_categories(self):
        return self._categories

    def set_categories(self, categories: List):
        self._categories = categories

    def __str__(self) -> str:
        return (
            f'Vacancy ID: {self._id}\n'
            f'Name: {self._name}\n'
            f'Department: {self._department}\n'
            f'Categories: {self._categories}\n'
        )


