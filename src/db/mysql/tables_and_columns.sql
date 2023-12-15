CREATE DATABASE skillsync;
USE skillsync;

CREATE TABLE applicant (
    id VARCHAR(36) NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    date_of_birth DATE NOT NULL,
    street VARCHAR(255) NOT NULL,
    postal_code VARCHAR(255) NOT NULL,
    city VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone_number VARCHAR(255) NOT NULL,
    face_image MEDIUMBLOB,
    PRIMARY KEY (id)
);

CREATE TABLE vacancy (
    id VARCHAR(36) NOT NULL,
    vacancy_title VARCHAR(255) NOT NULL,
    department VARCHAR(255) NOT NULL,
    full_time BOOLEAN NOT NULL,
    description TEXT NOT NULL,
    salary FLOAT NOT NULL,
    company VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    PRIMARY KEY (id)
);


CREATE TABLE rating (
    id VARCHAR(36) NOT NULL,
    category_id VARCHAR(36) NOT NULL,
    vacancy_id VARCHAR(36) NOT NULL,
    applicant_id VARCHAR(36) NOT NULL,
    score INT NOT NULL,
    justification TEXT NOT NULL,
    quote TEXT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (vacancy_id) REFERENCES vacancy(id)
);

CREATE TABLE applicant_vacancy (
    id INT AUTO_INCREMENT,
    applicant_id VARCHAR(36) NOT NULL,
    vacancy_id VARCHAR(36) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (applicant_id) REFERENCES applicant(id),
    FOREIGN KEY (vacancy_id) REFERENCES vacancy(id)
);