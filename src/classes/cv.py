from classes.business_object import BusinessObject


class CV(BusinessObject):

    def __init__(
            self,
            content
    ) -> None:
        super().__init__()
        self._content = content

    def get_content(self):
        return self._content

    def set_content(self, content):
        self._content = content

    def __str__(self) -> str:
        return (
            f'CV ID: {self._id}\n'
            f'Creation Date: {self._creation_date}\n'
            f'Content: {self._content}\n'
        )