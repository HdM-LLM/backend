from uuid import UUID
from classes.business_object import BusinessObject

class Rating(BusinessObject):

    def __init__(
        self,
        category_id: UUID,
        vacancy_id: UUID,
        applicant_id: UUID,
        score: int,
        justification: str,
        quote: str,
    )-> None:
        super().__init__()
        self._category_id = category_id
        self._vacancy_id = vacancy_id
        self._applicant_id = applicant_id
        self._score = score
        self._justification = justification
        self._quote = quote

    def get_category_id(self):
        return self._category_id

    def set_category_id(self, category_id: UUID):
        self._category_id = category_id

    def get_vacancy_id(self):
        return self._vacancy_id

    def set_vacancy_id(self, vacancy_id: UUID):
        self._vacancy_id = vacancy_id

    def get_applicant_id(self):
        return self._applicant_id

    def set_applicant_id(self, applicant_id: UUID):
        self._applicant_id = applicant_id

    def get_score(self):
        return self._score

    def set_score(self, score: int):
        self._score = score

    def get_justification(self):
        return self._justification

    def set_justification(self, justification: str):
        self._justification = justification

    def get_quote(self):
        return self._quote

    def set_quote(self, quote: str):
        self._quote = quote

    def __str__(self) -> str:
        return (
            f'Rating ID: {self._id}\n'
            f'Category ID: {self._category_id}\n'
            f'Vacancy ID: {self._vacancy_id}\n'
            f'Applicant ID: {self._applicant_id}\n'
            f'Score: {self._score}\n'
            f'Justification: {self._justification}\n'
            f'Quote: {self._quote}\n'
        )