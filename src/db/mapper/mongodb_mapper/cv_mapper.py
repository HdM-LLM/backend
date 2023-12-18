from db.mapper.mongodb_mapper.mongo_mapper import MongoMapper
from classes.applicant import Applicant
from classes.cv import CV
from uuid import UUID


class CVMapper(MongoMapper):

    """
    Creates an of CVMapper
    """

    def __init__(self, collection: str = 'csv'):
        super().__init__(collection)

    """
    Returns all the CVs from the db
    """
    def get_all(self):
        pass

    # Get specific cv by id
    def get_by_id(self, applicant_id: UUID):
        files = self.get_database().fs.files.find_one({'filename': str(applicant_id)})
        chunks = self.get_database().fs.chunks.find_one({'files_id': files['_id']})

        return chunks

    """
    Insert a CV into the db
    """
    def insert(self, cv: CV, applicant: Applicant) -> None:
        metadata = {
            'uuid': str(cv.get_id()),
            'type': 'CV',
            'applicant': {
                'first_name': str(applicant.get_first_name()),
                'last_name': str(applicant.get_last_name()),
                'email': str(applicant.get_email()),
            }
        }

        self.get_fs().put(cv.get_content().encode(), filename=str(applicant.get_id()), metadata=metadata)

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