from db.mapper.mongodb_mapper.mongo_mapper import MongoMapper
from classes.vacancy import Vacancy
from classes.category import Category
from uuid import uuid4, UUID


class VacancyMapper(MongoMapper):

    """
    Creates a instance of VacancyMapper
    """

    def __init__(self, collection: str = 'vacancies'):
        super().__init__(collection)

    def get_all(self):
        pass

    def get_by_id(self, vacancy_id: UUID) -> Vacancy:

        return

    def insert(self, vacancy_content: str, vacancy: Vacancy) -> None:
        """
        Insert vacancy content into the db
        """

        # Create metadata
        metadata = {
            "uuid": str(vacancy.get_id()),
            "type": "VACANCY",
            "applicant": {
                "id": str(vacancy.get_id()),
                "title": str(vacancy.get_title()),
            },
            "vacancy_id": str(vacancy.get_id()),
        }

        vacancy_encoding = vacancy_content.encode('utf-8')

        # Insert the cv into the db
        self.get_fs().put(vacancy_encoding, filename=str(vacancy.get_id()), metadata=metadata)
        pass

    def update(self):
        pass

    def delete_by_id(self, applicant_id: UUID):
        pass
