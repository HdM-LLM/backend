CREATE DATABASE skillsync;
USE skillsync;

CREATE TABLE applicants (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(100) NOT NULL,
    LastName VARCHAR(100) NOT NULL,
    DateOfBirth DATE NOT NULL,
    Street VARCHAR(100) NOT NULL,
    PostalCode VARCHAR(100) NOT NULL,
    City VARCHAR(100) NOT NULL,
    Email VARCHAR(100) NOT NULL,
    Phone VARCHAR(100) NOT NULL,
    Rating INT NOT NULL,
);

CREATE TABLE applicants_skills (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    applicant_id INT NOT NULL,
    skill_id INT NOT NULL,
    FOREIGN KEY (applicant_id) REFERENCES applicants(id),
    FOREIGN KEY (skill_id) REFERENCES skills(id)
);

CREATE TABLE skills (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Category INT NOT NULL,
    Rating INT NOT NULL,
    Applicant INT NOT NULL,
    FOREIGN KEY (Category) REFERENCES categories(id),
    FOREIGN KEY (Applicant) REFERENCES applicants(id)
);

CREATE TABLE rating(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Applicant INT NOT NULL,
    Category INT NOT NULL,
    Score INT NOT NULL,
    Justification VARCHAR(1000) NOT NULL,
    CV BLOB NOT NULL,
    FOREIGN KEY (Applicant) REFERENCES applicants(id)
    FOREIGN KEY (Category) REFERENCES categories(id)
);

INSERT INTO applicants (FirstName, LastName)
VALUES ('Max', 'Mustermann'), ('Lisa', 'Musterfrau');
