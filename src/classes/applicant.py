from uuid import UUID, uuid4
from datetime import date
from user import User


class Applicant(User):

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
            skills: list,
            rating: int,
    ) -> None:
        super().__init__(
            first_name=first_name,
            last_name=last_name
        )
        self._date_of_birth = date_of_birth
        self._street = street
        self._postal_code = postal_code
        self._city = city
        self._email = email
        self._phone_number = phone_number
        self._skills = skills
        self._rating = rating

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

    def get_skills(self) -> list:
        return self._skills
    
    def add_skill(self, skill) -> None:
        self._skills.append(skill)

    def set_score(self, skills) -> int:
        for skill in skills:
            self._rating = skill.get_rating()
            self._score += self._rating.get_score()
        self._score = self._score / len(skills)

    def get_score(self) -> int:
        return self._score

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
            f'Rating: {self._rating}'
        )
