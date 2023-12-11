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
    PRIMARY KEY (id)
);
