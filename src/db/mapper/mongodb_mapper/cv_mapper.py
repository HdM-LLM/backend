from db.mapper.mongodb_mapper.mongo_mapper import MongoMapper
from classes.applicant import Applicant
from classes.cv import CV
from uuid import UUID, uuid4
from werkzeug.datastructures import FileStorage


class CVMapper(MongoMapper):
    def __init__(self, collection: str = "fs.files"):
        """
        Creates an instance of CVMapper
        """
        super().__init__(collection)

    def get_all(self):
        """
        Returns all the CVs from the db
        """
        pass

    def get_by_id(self, applicant_id: str, vacancy_id: str):
        """
        Returns a CV by id
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
        """
        Insert a CV into the db
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
        """
        Update a CV from the db
        """
        pass

    def delete_by_id(self, applicant_id: UUID):
        """
        Deletes a CV from the db
        """
        pass
