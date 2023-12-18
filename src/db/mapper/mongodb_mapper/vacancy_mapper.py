from db.mapper.mongodb_mapper.mongo_mapper import MongoMapper
from classes.vacancy import Vacancy
from classes.category import Category
from uuid import UUID


class VacancyMapper(MongoMapper):

    """
    Creates a instance if VacancyMapper
    """
    def __init__(self, collection: str = 'vacancies'):
        super().__init__(collection)

    def get_all(self):
        pass

    def get_by_id(self, vacancy_id: UUID) -> Vacancy:
        result = self.get_collection().find_one({'uuid': str(vacancy_id)})

        vacancy = Vacancy(
            result['name'],
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
