from typing import List
from classes.business_object import BusinessObject


class Vacancy(BusinessObject):
    def __init__(
        self,
        title: str,
        department: str,
        fullTime: bool = True,
        description: str = "",
        salary: float = 0.0,
        company: str = "",
        createdAt: str = "",
        updatedAt: str = "",
    ) -> None:
        super().__init__()
        self._title = title
        self._department = department
        self._fullTime = fullTime
        self._description = description
        self._salary = salary
        self._company = company
        self._createdAt = createdAt
        self._updatedAt = updatedAt
        self._categories = []

    def get_title(self) -> str:
        return self._title

    def set_title(self, title: str) -> None:
        self._title = title

    def get_department(self) -> str:
        return self._department

    def set_department(self, department: str) -> None:
        self._department = department

    def get_full_time(self) -> bool:
        return self._fullTime

    def set_full_time(self, full_time: bool) -> None:
        self._fullTime = full_time

    def get_description(self) -> str:
        return self._description

    def set_description(self, description: str) -> None:
        self._description = description

    def get_salary(self) -> float:
        return self._salary

    def set_salary(self, salary: float) -> None:
        self._salary = salary

    def get_company(self) -> str:
        return self._company

    def set_company(self, company: str) -> None:
        self._company = company

    def get_created_at(self) -> str:
        return self._createdAt

    def set_created_at(self, created_at: str) -> None:
        self._createdAt = created_at

    def get_updated_at(self) -> str:
        return self._updatedAt

    def set_updated_at(self, updated_at: str) -> None:
        self._updatedAt = updated_at

    def get_categories(self) -> List:
        return self._categories

    def set_categories(self, categories: List) -> None:
        self._categories = categories

    def __str__(self) -> str:
        return (
            f'Vacancy ID: {self._id}\n'
            f'VacancyTitle: {self._vacancyTitle}\n'
            f'Department: {self._department}\n'
            f'Full Time: {self._fullTime}\n'
            f'Description: {self._description}\n'
            f'Salary: {self._salary}\n'
            f'Company: {self._company}\n'
            f'Created At: {self._createdAt}\n'
            f'Updated At: {self._updatedAt}\n'
            f'Categories: {self._categories}\n'
        )
