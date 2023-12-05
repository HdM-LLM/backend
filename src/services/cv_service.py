import PyPDF2
from datetime import date


# Returns the first name from inside the cv


def get_first_name_from_cv(cv_content: str) -> str:
    all_lines = cv_content.split('\n')
    specific_line: str

    for line in all_lines:
        if 'Name:' in line:
            specific_line = line

    first_name = specific_line.split(' ')[1]

    return first_name


# Returns the last name from inside the cv


def get_last_name_from_cv(cv_content: str) -> str:
    all_lines = cv_content.split('\n')
    specific_line: str

    for line in all_lines:
        if 'Name:' in line:
            specific_line = line

    last_name = specific_line.split(' ')[2]

    return last_name


# Returns the date of birth from inside the cv


def get_date_of_birth_from_cv(cv_content: str) -> date:
    all_lines = cv_content.split('\n')
    specific_line: str

    for line in all_lines:
        if 'Geburtsdatum / -ort:' in line:
            specific_line = line

    date_of_birth = specific_line.split(' ')[3].split('.')
    day = int(date_of_birth[0])
    month = int(date_of_birth[1])
    year = int(date_of_birth[2])

    return date(year, month, day)


# Returns the street from inside the cv


def get_street_from_cv(cv_content: str) -> str:
    all_lines = cv_content.split('\n')
    specific_line: str

    for line in all_lines:
        if 'Anschrift:' in line:
            specific_line = line

    street = specific_line.split(' ')[1]
    number = specific_line.split(' ')[2][:-1]

    return street + ' ' + number


# Returns the street from inside the cv


def get_street_from_cv(cv_content: str) -> str:
    all_lines = cv_content.split('\n')
    specific_line: str

    for line in all_lines:
        if 'Anschrift:' in line:
            specific_line = line

    street = specific_line.split(' ')[1]
    number = specific_line.split(' ')[2][:-1]

    return street + ' ' + number


# Returns the postal code from inside the cv


def get_postal_code_from_cv(cv_content: int) -> int:
    all_lines = cv_content.split('\n')
    specific_line: str

    for line in all_lines:
        if 'Anschrift:' in line:
            specific_line = line

    postal_code = specific_line.split(' ')[3]

    return postal_code


# Returns the city from inside the cv


def get_city_code_from_cv(cv_content: str) -> str:
    all_lines = cv_content.split('\n')
    specific_line: str

    for line in all_lines:
        if 'Anschrift:' in line:
            specific_line = line

    city = specific_line.split(' ')[4]

    return city


# Returns the email from inside the cv


def get_email_from_cv(cv_content: str) -> str:
    all_lines = cv_content.split('\n')
    specific_line: str

    for line in all_lines:
        if 'E-Mail Adresse:' in line:
            specific_line = line

    email = specific_line.split(' ')[2]

    return email


# Returns the phone number from inside the cv


def get_email_from_cv(cv_content: str) -> str:
    all_lines = cv_content.split('\n')
    specific_line: str

    for line in all_lines:
        if 'Telefonnummer:' in line:
            specific_line = line

    country_code = specific_line.split(' ')[1]
    national_area_code = specific_line.split(' ')[2]
    connection_identifier = specific_line.split(' ')[3]

    return country_code + ' ' + national_area_code + ' ' + connection_identifier
