from business_object import BusinessObject
from uuid import UUID, uuid4
from category import Category
from rating import Rating


class Skill(BusinessObject):
    """Class which represents a Skill inside the system

    Args:
        BusinessObject (BusinessObject): Inherits BusinessObject class
    """

    def __init__(
            self,
            category: Category,
            rating: Rating,
            applicant_id: uuid4,
    ) -> None:
        """Creates a instance of a Skill

        Args:
            category (Category): Category of a skill
            rating (Rating): Rating of a skill
            applicant_id (uuid4): Id of a applicant
        """
        super().__init__()
        self._category = category
        self._rating = rating
        self._applicant_id = applicant_id

    def get_category(self) -> Category:
        return self._category

    def set_category(self, category) -> None:
        self._category = category

    def get_rating(self) -> Rating:
        return self._rating

    def set_rating(self, rating) -> None:
        self._rating = rating

    def get_applicant_id(self) -> uuid4:
        return self._applicant_id

    def set_applicant_id(self, applicant_id) -> None:
        self._applicant_id = applicant_id
