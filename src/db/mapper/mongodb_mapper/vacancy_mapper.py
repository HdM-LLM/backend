from db.mapper.mapper import Mapper
from classes.vacancy import Vacancy
from classes.category import Category
from uuid import UUID
import pymongo
from gridfs import GridFS


client = pymongo.MongoClient('mongodb://root:password@localhost:27017/')
db = client['skillsync']
collection = db['vacancies']
fs = GridFS(db)


class VacancyMapper(Mapper):

    def __int__(self):
        super().__init__()

    def get_all(self):
        pass


    def get_by_id(self, vacancy_id: UUID) -> Vacancy:
        result = collection.find_one({'uuid': str(vacancy_id)})

        vacancy = Vacancy(
            str(result['name']),
            result['department']
        )

        vacancy.set_id(result['uuid'])

        categories = []

        for category in result['categories']:
            temp_category = Category(
                category['name'],
                category['guideline_0'],
                category['guideline_10']
            )

            temp_category.set_id(category['uuid'])

            categories.append(temp_category)

        vacancy.set_categories(categories)

        return vacancy

    def insert(self, cv_pdf_file) -> None:
        pass

    def update(self):
        pass

    def delete_by_id(self, applicant_id: UUID):
        pass
