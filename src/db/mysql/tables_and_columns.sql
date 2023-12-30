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

-- Erster Beispiel ASCDatensatz
INSERT INTO vacancy (
    id,
    vacancy_title,
    department,
    full_time,
    description,
    salary,
    company,
    created_at,
    updated_at
) VALUES (
    '6ca830b2-99b5-11ee-b9d1-0242ac120002',
    'Frontend Dev',
    'IT Deparment',
    TRUE, 
    'Description goes here',
    50000.00, 
    'Firmenname',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- Zweiter Beispiel Datensatz
INSERT INTO vacancy (
    id,
    vacancy_title,
    department,
    full_time,
    description,
    salary,
    company,
    created_at,
    updated_at
) VALUES (
    'dae80908-4cce-4d65-9357-ea48f7f2e4af',
    'Backend Dev',
    'IT Deparment',
    FALSE, 
    'Hier kann ihre Werbung stehen',
    35000.00,
    'Firmenname',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);
