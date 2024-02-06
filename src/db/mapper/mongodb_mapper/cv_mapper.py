from db.mapper.mongodb_mapper.mongo_mapper import MongoMapper
from classes.applicant import Applicant
from classes.cv import CV
from uuid import UUID, uuid4
from werkzeug.datastructures import FileStorage


class CVMapper(MongoMapper):
    """Class which implements a database mapper for the CVs

    Args:
        MongoMapper (MongoMapper): Inherits MongoMapper class
    """

    def __init__(self, collection: str = "fs.files") -> None:
        """Creates a instance of a CVMapper

        Args:
            collection (str, optional): Collection where the CVs should be stored
        """
        super().__init__(collection)

    def get_all(self) -> None:
        """Returns all the CVs from the db
        """
        pass

    def get_by_id(self, applicant_id: str, vacancy_id: str) -> tuple:
        """Returns the CV by its id from the databse

        Args:
            applicant_id (str): Id of the applicant
            vacancy_id (str): Id of the vacancy

        Returns:
            tuple: The CV
        """
        retrieved_cv = None
        try:
            retrieved_cv = self.get_fs().find_one(
                {
                    "metadata.applicant.id": applicant_id,
                    "metadata.vacancy_id": vacancy_id,
                }
            )
        except:
            print("Error while retrieving cv from db")

        retrieved_cv_bytes = retrieved_cv.read()

        return retrieved_cv.filename, retrieved_cv_bytes

    def insert(self, cv: FileStorage, applicant: Applicant, vacancy_id: str) -> None:
        """Inserts a CV into the database

        Args:
            cv (FileStorage): CV which should be inserted
            applicant (Applicant): Applicant of the CV
            vacancy_id (str): Id of the vacancy
        """
        # Generate a new random id
        # Do not use the applicant id, because one applicant can have multiple cv's
        generated_id = uuid4()

        # Create metadata
        metadata = {
            "uuid": str(generated_id),
            "type": "CV",
            "applicant": {
                "id": str(applicant.get_id()),
                "first_name": str(applicant.get_first_name()),
                "last_name": str(applicant.get_last_name()),
                "email": str(applicant.get_email()),
            },
            "vacancy_id": vacancy_id,
        }

        # Insert the cv into the db
        self.get_fs().put(cv, filename=cv.filename, metadata=metadata)

    def update(self, cv: CV):
        """Update a CV from the db
        """
        pass

    def delete_by_id(self, applicant_id: UUID):
        """Deletes a CV from the db
        """
        pass
