from db.mapper.mapper import Mapper
from classes.applicant import Applicant
from uuid import UUID

class CvMapper(Mapper):

    def __int__(self):
        super().__init__()

    def get_all(self):
        pass

    def get_by_id(self, cv_id: str):
        pass

    def insert(self, applicant: Applicant):
        pass

    def update_id(self, applicant_id: str):
        pass

    def delete_by_id(self, applicant_id: str):
        pass


