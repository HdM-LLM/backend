from db.mapper.mongodb_mapper.mongo_mapper import MongoMapper
from classes.vacancy import Vacancy
from classes.category import Category
from uuid import uuid4, UUID


class VacancyMapper(MongoMapper):
    """Class which implements a database mapper for the CVs

    Args:
        MongoMapper (MongoMapper): Inherits MongoMapper class
    """

    def __init__(self, collection: str = 'vacancies') -> None:
        """Creates a instance of a VacancyMapper

        Args:
            collection (str, optional): _description_. Collection where the Vacancies should be stored
        """
        super().__init__(collection)

    def get_all(self) -> None:
        """Returns all vacancies
        """
        pass

    def get_by_id(self, vacancy_id: UUID) -> Vacancy:
        """Returns vacancy id its id

        Args:
            vacancy_id (UUID): Id of the vacancy

        Returns:
            Vacancy: The vacancy
        """
        return

    def insert(self, vacancy_content: str, vacancy: Vacancy) -> None:
        """Inserts the content of a vacancy into the db

        Args:
            vacancy_content (str): The content of the vacancy
            vacancy (Vacancy): _description_
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

    def update(self) -> None:
        """Updates a vacancy inside the db
        """
        pass

    def delete_by_id(self, applicant_id: UUID) -> None:
        """Deletes a vacancy by its id

        Args:
            applicant_id (UUID): Id of the applicant
        """
        pass
