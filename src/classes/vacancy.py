from typing import List
from classes.business_object import BusinessObject
from enums.workingHour import WorkingHour
from enums.department import Department


class Vacancy(BusinessObject):
    """Class which represents a Vacancy inside the system

    Args:
        BusinessObject (BusinessObject): Inherits BusinessObject class
    """

    def __init__(
        self,
        title: str,
        department: Department,
        working_hours: WorkingHour,
        description: str = "",
    ) -> None:
        """_summary_

        Args:
            title (str): Title of the position
            department (Department): Department of the position
            working_hours (WorkingHour): Working hours of the position
            description (str, optional): Description of the position
        """
        super().__init__()
        self._title = title
        self._department = department
        self._working_hours = working_hours
        self._description = description
        self._categories = []

    def get_title(self) -> str:
        return self._title

    def set_title(self, title: str) -> None:
        self._title = title

    def get_department(self) -> str:
        return self._department

    def set_department(self, department: Department) -> None:
        self._department = department

    def get_working_hours(self) -> WorkingHour:
        return self._working_hours

    def set_working_hours(self, working_hours: WorkingHour) -> None:
        self._working_hours = working_hours

    def get_description(self) -> str:
        return self._description

    def set_description(self, description: str) -> None:
        self._description = description

    def get_categories(self) -> List:
        return self._categories

    def set_categories(self, categories: List) -> None:
        self._categories = categories

    def __str__(self) -> str:
        return (
            f'Vacancy ID: {self._id}\n'
            f'VacancyTitle: {self._title}\n'
            f'Department: {self._department}\n'
            f'Working Hours: {self._working_hours}\n'
            f'Description: {self._description}\n'
            f'Categories: {self._categories}\n'
        )
