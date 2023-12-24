from db.mapper.mysql_mapper.mysql_mapper import MySQLMapper
from classes.vacancy import Vacancy
from uuid import UUID


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
                department=row[2],
                fullTime=row[3],
                description=row[4],
                salary=row[5],
                company=row[6],
                createdAt=row[7],
                updatedAt=row[8],
            )
            vacancy.set_id(row[0])
            vacancies.append(vacancy)

        cursor.close()
        return vacancies

    def get_by_id(self, vacancy_id: UUID):
        cursor = self._connection.cursor()
        query = "SELECT * FROM vacancy WHERE id = %s"
        cursor.execute(query, (str(vacancy_id),))

        row = cursor.fetchone()
        if row:
            vacancy = Vacancy(
                title=row[1],
                department=row[2],
                fullTime=row[3],
                description=row[4],
                salary=row[5],
                company=row[6],
                createdAt=row[7],
                updatedAt=row[8],
            )
            vacancy.set_id(row[0])
            cursor.close()
            return vacancy
        else:
            cursor.close()
            return None

    def insert(self, vacancy: Vacancy):
        cursor = self._connection.cursor()
        query = "INSERT INTO vacancy (id, vacancy_title, department, full_time, description, salary, company, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        data = (
            str(vacancy.get_id()),
            vacancy.get_title(),
            vacancy.get_department(),
            vacancy.get_full_time(),
            vacancy.get_description(),
            vacancy.get_salary(),
            vacancy.get_company(),
            vacancy.get_created_at(),
            vacancy.get_updated_at(),
        )

        cursor.execute(query, data)

        self._connection.commit()
        cursor.close()

    def update(self, vacancy: Vacancy):
        pass

    def delete_by_id(self, vacancy_id: UUID):
        pass
