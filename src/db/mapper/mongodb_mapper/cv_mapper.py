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

    def __int__(self):
        super().__init__()

    def get_all(self):
        result = fs.find()

        return result

    def get_by_id(self, applicant_id: UUID):
        result = fs.find_one({'filename': str(applicant_id)})

        return result

    def insert(self, cv_pdf_file, applicant: Applicant) -> None:
        metadata = {
            'type': 'CV',
            'applicant': {
                'first_name': str(applicant.get_first_name()),
                'last_name': str(applicant.get_last_name()),
                'email': str(applicant.get_email()),
            }
        }

        fs.put(cv_pdf_file, filename=str(applicant.get_id()), metadata=metadata)

    def update(self, cv: CV):
        pass

    def delete_by_id(self, applicant_id: UUID):
        file_to_delete = fs.find_one({'uuid': str(applicant_id)})

        # Delete the file
        fs.delete(file_to_delete._id)
