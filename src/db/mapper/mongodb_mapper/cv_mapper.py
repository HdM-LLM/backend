import random
from db.mapper.mongodb_mapper.mongo_mapper import MongoMapper
from classes.applicant import Applicant
from classes.cv import CV
from uuid import UUID
from werkzeug.datastructures import FileStorage


class CVMapper(MongoMapper):

    """
    Creates an instance of CVMapper
    """

    def __init__(self, collection: str = 'fs.files'):
        super().__init__(collection)

    """
    Returns all the CVs from the db
    """

    def get_all(self):
        pass

    # Get specific cv by email
    # TODO: add vacancy (id?) to the query to get the cv for a specific vacancy (one applicant can have multiple cv's for different vacancies)
    def get_by_email(self, applicant_email: str):
        file = self.get_collection().find(
            {'applicant.email': applicant_email})

    """
    Insert a CV into the db
    """

    def insert(self, cv: FileStorage, applicant: Applicant, vacancy_id: str) -> None:

        # Generate a new id from a random 128 bit integer
        generated_id = UUID(random.getrandbits(128))

        # Create metadata
        metadata = {
            'uuid': str(generated_id),
            'type': 'CV',
            'applicant': {
                'first_name': str(applicant.get_first_name()),
                'last_name': str(applicant.get_last_name()),
                'email': str(applicant.get_email()),
            }
        }

        # Create file name
        filename = str(applicant.get_id()) + '&' + vacancy_id

        # Insert the cv into the db
        self.get_fs().put(cv.stream, filename=filename, metadata=metadata)

    """
    Update a CV from the db
    """

    def update(self, cv: CV):
        pass

    """
    Deletes a CV from the db
    """

    def delete_by_id(self, applicant_id: UUID):
        pass
