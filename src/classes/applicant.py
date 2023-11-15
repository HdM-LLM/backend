from uuid import UUID, uuid4
import datetime


class Applicant():

    def __init__(
            self,
            first_name: str,
            last_name: str,
            date_of_birth: datetime.date,
            street: str,
            postal_code: int,
            city: str,
            email: str,
            phone_number: int,
            rating: float = 0.0
    ) -> None:
        self._id = uuid4()
        self._first_name = first_name
        self._last_name = last_name
        self._data_of_birth = date_of_birth
        self._street = street
        self._postal_code = postal_code
        self._city = city
        self._email = email
        self._phone_number = phone_number
        self._rating = rating

    def get_id(self) -> UUID:
        return self._id

    def get_first_name(self) -> str:
        return self._first_name

    def set_first_name(self, first_name):
        self._first_name = first_name

    def get_last_name(self) -> str:
        return self._last_name

    def set_last_name(self, last_name):
        self._last_name = last_name

    def get_date_of_birth(self):
        return self._date_of_birth

    def set_date_of_birth(self, date_of_birth):
        self._date_of_birth = date_of_birth

    def get_street(self):
        return self._street

    def set_street(self, street):
        self._street = street

    def get_postal_code(self):
        return self._postal_code

    def set_postal_code(self, postal_code):
        self._postal_code = postal_code

    def get_city(self):
        return self._city

    def set_city(self, city):
        self._city = city

    def get_email(self):
        return self._email

    def set_email(self, email):
        self._email = email

    def get_phone_number(self):
        return self._phone_number

    def set_phone_number(self, phone_number):
        self._phone_number = phone_number

    def get_rating(self):
        return self._rating

    def set_rating(self, rating):
        self._rating = rating


p = Applicant('a',
              'a',
              datetime.date(1999, 1, 1),
              'a', 1234,
              'a',
              'a',
              1234)

print(p.get_rating())
