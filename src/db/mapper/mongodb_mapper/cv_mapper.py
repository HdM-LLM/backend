from db.mapper.mapper import Mapper
from classes.applicant import Applicant
from uuid import UUID

class CvMapper(Mapper):

    def __int__(self):
        super().__init__()

    def get_all(self):
        pass

    def get_by_id(self, cv_id: UUID):
        pass

    def insert(self, applicant: Applicant):
        pass

    def update(self, applicant: Applicant):
        pass

    def delete_by_id(self, applicant_id: UUID):
        pass


