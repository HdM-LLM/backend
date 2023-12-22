from db.mapper.mysql_mapper.mysql_mapper import MySQLMapper
from classes.applicant import Applicant
from uuid import UUID


class ApplicantMapper(MySQLMapper):

    def __int__(self):
        super().__init__()

    def get_all(self):
        result = []
        cursor = self._connection.cursor()
        cursor.execute("""
            SELECT * FROM applicant
        """)

        tuples = cursor.fetchall()

        for tuple_data in tuples:
            (id, first_name, last_name, date_of_birth, street, postal_code,
             city, email, phone_number, face_image) = tuple_data
            applicant = Applicant(first_name, last_name, date_of_birth,
                                  street, postal_code, city, email, phone_number, face_image)
            applicant.set_id(UUID(id))
            result.append(applicant)

        self._connection.commit()
        cursor.close()
        return result

    def get_by_id(self, applicant_id: UUID):
        result = []
        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT * FROM applicant WHERE id='{}'".format(applicant_id))
        tuples = cursor.fetchall()
        try:
            (id, first_name, last_name, date_of_birth, street,
             postal_code, city, email, phone_number, face_image) = tuples[0]
            applicant = Applicant(first_name, last_name, date_of_birth,
                                  street, postal_code, city, email, phone_number, face_image)
            applicant.set_id(UUID(id))
            result = applicant

        except IndexError:
            result = None

        self._connection.commit()
        cursor.close()
        return result

    def get_by_email(self, applicant_email: str):
        result = []
        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT * FROM applicant WHERE email='{}'".format(applicant_email))
        tuples = cursor.fetchall()
        try:
            (id, first_name, last_name, date_of_birth, street,
             postal_code, city, email, phone_number) = tuples[0]
            applicant = Applicant(first_name, last_name, date_of_birth,
                                  street, postal_code, city, email, phone_number)
            applicant.set_id(UUID(id))
            result = applicant

        except IndexError:
            result = None

        self._connection.commit()
        cursor.close()
        return result

    def get_by_vacancy_id(self, vacancy_id: UUID):
        result = []
        cursor = self._connection.cursor()
        cursor.execute("""
            SELECT a.*
            FROM applicant a
            JOIN applicant_vacancy av ON a.id = av.applicant_id
            WHERE av.vacancy_id = %s
        """, (str(vacancy_id),))

        tuples = cursor.fetchall()

        for tuple_data in tuples:
            (id, first_name, last_name, date_of_birth, street, postal_code,
             city, email, phone_number, face_image) = tuple_data
            applicant = Applicant(first_name, last_name, date_of_birth,
                                  street, postal_code, city, email, phone_number, face_image)
            applicant.set_id(UUID(id))
            result.append(applicant)

        self._connection.commit()
        cursor.close()
        return result

    def _insert_into_applicant_vacancy(self, applicant_id: UUID, vacancy_id: UUID):
        cursor = self._connection.cursor()
        query = """
            INSERT INTO applicant_vacancy (applicant_id, vacancy_id) 
            VALUES (%s, %s)
        """
        data = (
            str(applicant_id),
            str(vacancy_id)
        )

        cursor.execute(query, data)
        self._connection.commit()
        cursor.close()

    def insert(self, applicant: Applicant, vacancy_id: UUID):
        cursor = self._connection.cursor()
        query = """
            INSERT INTO applicant (
                id, first_name, last_name, date_of_birth, street, postal_code, city, email, phone_number, face_image
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        data = (
            str(applicant.get_id()),
            applicant.get_first_name(),
            applicant.get_last_name(),
            applicant.get_date_of_birth(),
            applicant.get_street(),
            applicant.get_postal_code(),
            applicant.get_city(),
            applicant.get_email(),
            applicant.get_phone_number(),
            applicant.get_face_image()
        )

        cursor.execute(query, data)
        self._connection.commit()
        cursor.close()

        # Aufruf der Funktion, um Daten in die applicant_vacancy-Tabelle einzufügen
        self._insert_into_applicant_vacancy(applicant.get_id(), vacancy_id)

    def update(self, applicant: Applicant):
        pass

    def delete_by_id(self, applicant_id: UUID):
        pass
