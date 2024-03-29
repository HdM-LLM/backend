from uuid import UUID
from datetime import date
from classes.user import User

class Applicant(User):
    """Class which represents a applicant inside the system

    Args:
        User (User): Inherits Use class
    """

    def __init__(
            self,
            first_name: str,
            last_name: str,
            date_of_birth: date,
            street: str,
            postal_code: int,
            city: str,
            email: str,
            phone_number: str,
            face_image: bytes = None,
    ) -> None:
        """Creates instance of a applicant

        Args:
            first_name (str): First name of the applicant
            last_name (str): Last name of the applicant
            date_of_birth (date): Date of birth of the applicant
            street (str): Street where the applicant lives
            postal_code (int): Postal code of the city where the applicant lives
            city (str): City where the applicant lives
            email (str): Email of the applicant
            phone_number (str): Phone number of the applicant
            face_image (bytes, optional): Picture of the applicant
        """
        super().__init__(first_name=first_name, last_name=last_name)
        self._date_of_birth = date_of_birth
        self._street = street
        self._postal_code = postal_code
        self._city = city
        self._email = email
        self._phone_number = phone_number
        self._face_image = face_image

    def get_date_of_birth(self) -> date:
        return self._date_of_birth

    def set_date_of_birth(self, date_of_birth) -> None:
        self._date_of_birth = date_of_birth

    def get_street(self) -> str:
        return self._street

    def set_street(self, street) -> None:
        self._street = street

    def get_postal_code(self) -> int:
        return self._postal_code

    def set_postal_code(self, postal_code) -> None:
        self._postal_code = postal_code

    def get_city(self) -> str:
        return self._city

    def set_city(self, city) -> None:
        self._city = city

    def get_email(self) -> str:
        return self._email

    def set_email(self, email) -> None:
        self._email = email

    def get_phone_number(self) -> str:
        return self._phone_number

    def set_phone_number(self, phone_number) -> None:
        self._phone_number = phone_number

    def get_face_image(self) -> bytes:
        return self._face_image

    def set_face_image(self, face_image: bytes) -> None:
        self._face_image = face_image

    def __str__(self) -> str:
        return (
            f'Person ID: {self._id}\n'
            f'First name: {self._first_name}\n'
            f'Last name: {self._last_name}\n'
            f'Date of Birth: {self._date_of_birth}\n'
            f'Street: {self._street}\n'
            f'Postal Code: {self._postal_code}\n'
            f'City: {self._city}\n'
            f'Email: {self._email}\n'
            f'Phone Number: {self._phone_number}\n'
        )
