CREATE DATABASE skillsync;
USE skillsync;

CREATE TABLE users (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(100) NOT NULL,
    LastName VARCHAR(100) NOT NULL
);

INSERT INTO users (FirstName, LastName)
VALUES ('Max', 'Mustermann'), ('Lisa', 'Musterfrau');
