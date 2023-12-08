from business_object import BusinessObject
from category import Category

class Rating(BusinessObject):

    def __init__(
        self,
        applicant_id: int,
        category: Category,
        score: int,
        justification: str, 
        cv: str,
    )-> None:
        super().__init__()
        self._applicant_id = applicant_id
        self._category = category
        self._score = score
        self._justification = justification
        self._cv = cv

    def get_applicant_id(self) -> int:
        return self._applicant_id
    
    def set_applicant_id(self, applicant_id) -> None:
        self._applicant_id = applicant_id

    def get_category(self) -> Category:
        return self._category

    def set_category(self, category) -> None:
        self._category = category

    def get_score(self) -> int:
        return self._score
    
    def set_score(self, score) -> None:
        self._score = score

    def get_justification(self) -> str:
        return self._justification
    
    def set_justification(self, justification) -> None:
        self._justification = justification

    def get_cv(self) -> str:
        return self._cv
    
    def set_cv(self, cv) -> None:
        self._cv = cv
    