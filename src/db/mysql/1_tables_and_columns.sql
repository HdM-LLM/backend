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
    total_score DECIMAL(5,2),
    PRIMARY KEY (id)
);

CREATE TABLE vacancy (
    id VARCHAR(36) NOT NULL,
    vacancy_title VARCHAR(255) NOT NULL,
    department ENUM('IT', 'HR', 'Marketing', 'Sales', 'Finance', 'Legal', 'Other') NOT NULL,
    working_hours ENUM('Fulltime', 'Parttime') NOT NULL,
    description TEXT NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE category (
    id VARCHAR(36) NOT NULL,
    name VARCHAR(255) NOT NULL,
    chip VARCHAR(255) NOT NULL,
    guideline_for_zero VARCHAR(255) NOT NULL,
    guideline_for_ten VARCHAR(255) NOT NULL,
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

CREATE TABLE vacancy_category (
    id INT AUTO_INCREMENT,
    vacancy_id VARCHAR(36) NOT NULL,
    category_id VARCHAR(36) NOT NULL,
    weight FLOAT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (category_id) REFERENCES category(id),
    FOREIGN KEY (vacancy_id) REFERENCES vacancy(id)
);

CREATE TABLE employee (
    id VARCHAR(36) NOT NULL,
    first_name varchar(255) NOT NULL,
    last_name varchar(255) NOT NULL,
    email varchar(100) NOT NULL,
    phone_number varchar(20) NOT NULL,
    face_image MEDIUMBLOB,
    created_at timestamp NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE evaluation (
    id VARCHAR(36) NOT NULL,
    applicant_id VARCHAR(36) NOT NULL,
    score INT NOT NULL CHECK (score >= 0 AND score <= 10),
    PRIMARY KEY (id),
    FOREIGN KEY (applicant_id) REFERENCES applicant(id)
);

