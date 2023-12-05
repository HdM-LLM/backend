CREATE DATABASE skillsync;
USE skillsync;

CREATE TABLE applicants (
    id VARCHAR(100) NOT NULL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    date_of_birth DATE NOT NULL,
    street VARCHAR(100) NOT NULL,
    postal_code VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone VARCHAR(100) NOT NULL,
    rating INT NOT NULL,
);

CREATE TABLE applicants_skills (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    applicant_id INT NOT NULL,
    skill_id INT NOT NULL,
    FOREIGN KEY (applicant_id) REFERENCES applicants(id),
    FOREIGN KEY (skill_id) REFERENCES skills(id)
);

CREATE TABLE skills (
    id VARCHAR(100) NOT NULL PRIMARY KEY,
    category VARCHAR(100) NOT NULL,
    rating INT NOT NULL,
    applicant VARCHAR(100) NOT NULL,
    FOREIGN KEY (Category) REFERENCES categories(id),
    FOREIGN KEY (Applicant) REFERENCES applicants(id)
);

CREATE TABLE rating(
    id VARCHAR(100) NOT NULL PRIMARY KEY,
    applicant VARCHAR(100) NOT NULL,
    category VARCHAR(100) NOT NULL,
    score INT NOT NULL,
    justification VARCHAR(1000) NOT NULL,
    FOREIGN KEY (Applicant) REFERENCES applicants(id)
    FOREIGN KEY (Category) REFERENCES categories(id)
);

INSERT INTO applicants (first_name, last_name)
VALUES ('Max', 'Mustermann'), ('Lisa', 'Musterfrau');
