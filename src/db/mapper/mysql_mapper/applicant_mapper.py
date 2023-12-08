from db.mapper.mapper import Mapper
from classes.applicant import Applicant
from uuid import UUID

class ApplicantMapper(Mapper):

    def __int__(self):
        super().__init__()

    def get_all(self):
        pass

    def get_by_id(self, applicant_id: UUID):
        pass

    def get_by_email(self, applicant_email: str):
        result = []
        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM applicant WHERE email='{}'".format(applicant_email))
        tuples = cursor.fetchall()
        try:
            (id, first_name, last_name, date_of_birth, street, postal_code, city, email, phone_number) = tuples[0]
            applicant = Applicant(first_name, last_name, date_of_birth, street, postal_code, city, email, phone_number)
            applicant.set_id(UUID(id))
            result = applicant

        except IndexError:
            result = None

        self._connection.commit()
        cursor.close()
        return result

    def insert(self, applicant: Applicant):
        cursor = self._connection.cursor()
        query = "INSERT INTO applicant (id, first_name, last_name, date_of_birth, street, postal_code, city, email, phone_number) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        data = (
            str(applicant.get_id()),
            applicant.get_first_name(),
            applicant.get_last_name(),
            applicant.get_date_of_birth(),
            applicant.get_street(),
            applicant.get_postal_code(),
            applicant.get_city(),
            applicant.get_email(),
            applicant.get_phone_number()
        )

        cursor.execute(query, data)

        self._connection.commit()
        cursor.close()

    def update(self, applicant: Applicant):
        pass

    def delete_by_id(self, applicant_id: UUID):
        pass


