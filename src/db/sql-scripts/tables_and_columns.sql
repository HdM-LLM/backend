CREATE DATABASE skillsync;
USE skillsync;

CREATE TABLE users (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(100) NOT NULL,
    LastName VARCHAR(100) NOT NULL
);

#CREATE TABLE job_postings (
#    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
#    position VARCHAR(255) NOT NULL,
#    description TEXT,
#    creation_date DATE,
#    start_date DATE,
#    department VARCHAR(100),
#    applicant VARCHAR(100) NOT NULL
#);

#CREATE TABLE applicants (
#    id INT AUTO_INCREMENT PRIMARY KEY,
#    first_name VARCHAR(255) NOT NULL,
#    last_name VARCHAR(255) NOT NULL,
#    phone_number VARCHAR(255) NOT NULL,
#    email_address VARCHAR(255) NOT NULL,
#    position_id INT NOT NULL,
#    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#    FOREIGN KEY (position_id) REFERENCES job_postings(id)
#);


#CREATE TABLE applicant_ratings (
#    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
#    applicant_id INT NOT NULL,
#    category VARCHAR(255) NOT NULL,
#    score INT NOT NULL,
#    justification TEXT,
#    quote TEXT,
#    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#    FOREIGN KEY (applicant_id) REFERENCES applicants(id)
#);


#CREATE TABLE job_categories (
#    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
#    category_name VARCHAR(100) NOT NULL,
#    guideline_0 TEXT,
#    guideline_10 TEXT
#);

#CREATE TABLE job_posting_categories (
#    job_posting_id INT NOT NULL,
#    category_id INT NOT NULL,
#    PRIMARY KEY (job_posting_id, category_id),
#    FOREIGN KEY (job_posting_id) REFERENCES job_postings(id),
#    FOREIGN KEY (category_id) REFERENCES job_categories(id)
#);

INSERT INTO users (FirstName, LastName)
VALUES ('Max', 'Mustermann'), ('Lisa', 'Musterfrau');

#INSERT INTO job_postings (
#    position,
#    description,
#    creation_date,
#    start_date,
#    department,
#    applicant
#) VALUES (
#    'java backend developer',
#    'Description of the position...',
#    '2023-01-01',
#    '2023-02-01',
#    'IT Department',
#    'John Doe'
#), (
#    '(Junior) IT System Engineer specializing in IT Networking (w/m/d)',
#    'Description of the position...',
#    '2023-02-01',
#    '2023-03-01',
#    'Networking Department',
#    'Jane Smith'
#);

#INSERT INTO job_categories (
#    category_name,
#    guideline_0,
#    guideline_10
#) VALUES (
#    'Coding Skills',
#    'Does not mention any coding-related experiences or skills.',
#    'Highlights extensive coding experiences, showcasing expertise in languages like Python and Java.'
#), (
#    'Communication Skills',
#    'Lacks examples of clear and concise communication in professional contexts.',
#    'Provides multiple instances of clear and effective communication in professional contexts.'
#), (
#    'Teamwork',
#    'Does not mention any collaborative projects or teamwork experiences.',
#    'Highlights various collaborative projects, demonstrating the ability to work effectively in a team.'
#), (
#    'Networking Expertise',
#    'Does not mention any experiences related to networking concepts or projects.',
#    'Provides detailed experiences and achievements in networking, showcasing in-depth knowledge.'
#), (
#    'Problem-Solving',
#    'Does not mention any experiences where problem-solving was essential.',
#    'Highlights various instances where problem-solving skills were crucial, providing detailed examples.'
#);

#INSERT INTO job_posting_categories (job_posting_id, category_id) VALUES
#(1, 1),
#(1, 2),
#(1, 3),
#(2, 4),
#(2, 5);
