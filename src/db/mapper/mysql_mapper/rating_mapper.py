from db.mapper.mapper import Mapper
from classes.rating import Rating
from uuid import UUID

class RatingMapper(Mapper):

    def __int__(self):
        super().__init__()

    def get_all(self):
        pass

    def get_by_id(self, applicant_id: UUID):
        pass

    def insert(self, rating: Rating):
        cursor = self._connection.cursor()
        query = "INSERT INTO rating (id, category_id, vacancy_id, applicant_id, score, justification, quote) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        data = (
            str(rating.get_id()),
            str(rating.get_category_id()),
            str(rating.get_vacancy_id()),
            str(rating.get_applicant_id()),
            rating.get_score(),
            rating.get_justification(),
            rating.get_quote(),
        )

        cursor.execute(query, data)

        self._connection.commit()
        cursor.close()

    def update(self, rating: Rating):
        pass

    def delete_by_id(self, rating_id: UUID):
        pass


