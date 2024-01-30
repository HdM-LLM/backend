from db.mapper.mysql_mapper.mysql_mapper import MySQLMapper
from classes.rating import Rating
from uuid import UUID


class RatingMapper(MySQLMapper):

    def __int__(self):
        super().__init__()

    def get_all(self):
        pass

    def get_by_id(self, vacancy_id: str, applicant_id: str):
        result = []
        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT * FROM rating WHERE vacancy_id='{}' AND applicant_id='{}'".format(vacancy_id, applicant_id))
        tuples = cursor.fetchall()

        for tuple_data in tuples:
            (id, category_id, vacancy_id, applicant_id,
             score, justification, quote, weight) = tuple_data

            rating = Rating(category_id, vacancy_id,
                            applicant_id, score, justification, quote, weight)
            rating.set_id(UUID(id))
            result.append(rating)

        self._connection.commit()
        cursor.close()

        return result

    def insert(self, rating: Rating):
        cursor = self._connection.cursor()
        query = "INSERT INTO rating (id, category_id, vacancy_id, applicant_id, score, justification, quote, weight) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        data = (
            str(rating.get_id()),
            str(rating.get_category_id()),
            str(rating.get_vacancy_id()),
            str(rating.get_applicant_id()),
            rating.get_score(),
            rating.get_justification(),
            rating.get_quote(),
            rating.get_weight(),
        )

        cursor.execute(query, data)

        self._connection.commit()
        cursor.close()

    def update(self, rating: Rating):
        pass

    def delete_by_id(self, rating_id: UUID):
        pass
