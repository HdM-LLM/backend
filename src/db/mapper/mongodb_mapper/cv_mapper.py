from db.mapper.mapper import Mapper
from classes.applicant import Applicant
from classes.cv import CV
from uuid import UUID
import pymongo
from typing import List
from gridfs import GridFS


client = pymongo.MongoClient('mongodb://root:password@localhost:27017/')
db = client['skillsync']
collection = db['cvs']
fs = GridFS(db)


class CVMapper(Mapper):

    """
    Creates an of CVMapper
    """
    def __int__(self):
        super().__init__()

    """
    Returns all the CVs from the db
    """
    def get_all(self):
        pass

    # Get specific cv by id
    def get_by_id(self, applicant_id: UUID):
        files = db.fs.files.find_one({'filename': str(applicant_id)})
        chunks = db.fs.chunks.find_one({'files_id': files['_id']})

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

        fs.put(cv.get_content().encode(), filename=str(applicant.get_id()), metadata=metadata)

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
