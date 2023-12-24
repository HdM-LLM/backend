from classes.business_object import BusinessObject


class Category(BusinessObject):

    def __init__(
        self,
        name: str,
        guideline_for_zero: str,
        guideline_for_ten: str,
    ) -> None:
        super().__init__()
        self._name = name
        self._guideline_for_zero = guideline_for_zero
        self._guideline_for_ten = guideline_for_ten

    def get_name(self) -> str:
        return self._name

    def set_name(self, name) -> None:
        self._name = name

    def get_guideline_for_zero(self) -> str:
        return self._guideline_for_zero

    def set_guideline_for_zero(self, guideline_for_zero) -> None:
        self._guideline_for_zero = guideline_for_zero

    def get_guideline_for_ten(self) -> str:
        return self._guideline_for_ten

    def set_guideline_for_ten(self, guideline_for_ten) -> None:
        self._guideline_for_ten = guideline_for_ten

    def __str__(self) -> str:
        return (
            f'Category ID: {self._id}\n'
            f'Name: {self._name}\n'
            f'Guideline 0: {self._guideline_for_zero}\n'
            f'Guideline 10: {self._guideline_for_ten}\n'
        )
