from db.mapper.mysql_mapper.mysql_mapper import MySQLMapper
from db.mapper.mysql_mapper.category_mapper import CategoryMapper
from classes.vacancy import Vacancy
from classes.category import Category
from uuid import UUID
from enums.workingHour import WorkingHour
from enums.department import Department


class VacancyMapper(MySQLMapper):

    def __init__(self):
        super().__init__()

    def get_all(self):
        cursor = self._connection.cursor()
        query = "SELECT * FROM vacancy"
        cursor.execute(query)

        vacancies = []
        for row in cursor.fetchall():
            vacancy = Vacancy(
                title=row[1],
                department=Department[row[2].upper()].value,
                working_hours=WorkingHour[row[3].upper()].value,
                description=row[4],
            )
            vacancy.set_id(row[0])
            vacancies.append(vacancy)

        cursor.close()
        return vacancies

    def get_all_categories_by_vacancy_id(self, vacancy_id: UUID):
        cursor = self._connection.cursor()
        query = "SELECT * FROM vacancy_category WHERE vacancy_id = %s;"
        cursor.execute(query, (str(vacancy_id),))

        categories = []

        for row in cursor.fetchall():
            with CategoryMapper() as category_mapper:
                return_value = category_mapper.get_by_id(row[2])
                # TODO: Check row[3] is the weight, when you want to retrieve it

                categories.append(return_value)

        return categories

    def get_by_id(self, vacancy_id: UUID):
        cursor = self._connection.cursor()
        query = "SELECT * FROM vacancy WHERE id = %s"
        cursor.execute(query, (str(vacancy_id),))

        row = cursor.fetchone()
        if row:
            vacancy = Vacancy(
                title=row[1],
                department=Department[row[2].upper()].value,
                working_hours=WorkingHour[row[3].upper()].value,
                description=row[4],
            )
            vacancy.set_id(row[0])
            cursor.close()
            return vacancy
        else:
            cursor.close()
            return None

    def insert(self, vacancy: Vacancy):
        cursor = self._connection.cursor()
        query = "INSERT INTO vacancy (id, vacancy_title, department, working_hours, description) VALUES (%s, %s, %s, %s, %s)"
        data = (
            str(vacancy.get_id()),
            vacancy.get_title(),
            Department[vacancy.get_department().upper()].value,
            WorkingHour[vacancy.get_working_hours().upper()].value,
            vacancy.get_description(),
        )

        cursor.execute(query, data)

        self._connection.commit()
        cursor.close()

    def insert_vacancy_category_relation(self, vacancy: Vacancy, category: Category):
        cursor = self._connection.cursor()
        query = "INSERT INTO vacancy_category (vacancy_id, category_id) VALUES (%s, %s %s)"
        data = (
            str(vacancy.get_id()),
            str(category.get_id()),
            # TODO: Add weight to data of query
        )

        cursor.execute(query, data)

        self._connection.commit()
        cursor.close()

    def update(self, vacancy: Vacancy):
        pass

    def delete_by_id(self, vacancy_id: UUID):
        pass
