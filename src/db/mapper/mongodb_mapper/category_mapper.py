from db.mapper.mongodb_mapper.mongo_mapper import MongoMapper
from classes.vacancy import Vacancy
from classes.category import Category
from uuid import UUID


class CategoryMapper(MongoMapper):

    """
    Creates a instance of CategoryMapper
    """

    def __init__(self, collection: str = 'vacancies'):
        super().__init__(collection)

    def get_all(self):
        pass

    def get_by_id(self, category_id: str) -> Category:
        result = self.get_collection().find_one(
            {}, {'categories': {'$elemMatch': {'uuid': category_id}}})

        category = Category(
            result['categories'][0]['name'],
            result['categories'][0]['guideline_0'],
            result['categories'][0]['guideline_10']
        )

        category.set_id(result['categories'][0]['uuid'])

        return category

    def insert(self, cv_pdf_file) -> None:
        pass

    def update(self):
        pass

    def delete_by_id(self, applicant_id: UUID):
        pass
