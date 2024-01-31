USE skillsync;

-- Example vacancies
INSERT INTO vacancy (
    id,
    vacancy_title,
    department,
    working_hours,
    description
) VALUES (
    '6ca830b2-99b5-11ee-b9d1-0242ac120002',
    'Frontend Developer',
    'IT',
    'FULLTIME',
    'We are looking for a frontend developer to join our team. You will be working with a team of highly skilled developers to build a scalable and secure frontend.'
);

INSERT INTO vacancy (
    id,
    vacancy_title,
    department,
    working_hours,
    description
) VALUES (
    'dae80908-4cce-4d65-9357-ea48f7f2e4af',
    'Backend Developer',
    'IT',
    'PARTTIME',
    'Your expertise is needed to build the next generation of our product. You will be working with a team of highly skilled developers to build a scalable and secure backend.'
);

-- Example categories

INSERT INTO category (
    id,
    name,
    chip,
    guideline_for_zero,
    guideline_for_ten
) VALUES 
-- Programming Language
(
    '025f2219-c03d-48b7-94b9-5c0557e21745',
    'Javascript',
    'Programming Language',
    'Does not mention any Javascript coding related experiences or skills',
    'Highlights extensive coding experiences, showcasing expertise in Javascript.'
),
(
    '9d44632c-a079-46bd-9100-09fb9dade3ec',
    'Java',
    'Programming Language',
    'Does not mention any Java coding related experiences or skills',
    'Highlights extensive coding experiences, showcasing expertise in Java.'
),
-- Soft Skills
(
    '24023f40-023a-4f26-85aa-193b5a0574f1',
    'Teamwork',
    'Soft Skills',
    'Does not mention any collaborative projects or teamwork experiences.',
    'Highlights various collaborative projects, demonstrating the ability to work effectively in a team.'
),
(
    '25043f40-023a-4f26-85aa-193b5a0574f1',
    'Leadership Skills',
    'Soft Skills',
    'No evidence of leadership abilities or experiences.',
    'Demonstrates strong leadership skills with a track record of successfully leading and motivating teams.'
),
-- Education
(
    'adbc65fe-90a0-4e0b-82cf-8c8ff6e16594',
    'Engineering Degree',
    'Education',
    'No formal education or a degree in another field than Engineering.',
    'Ph.D. in Engineering with an exceptional academic record.'
),
(
    '24023f40-023a-4f26-85aa-193b5a0574f2', 
    'Computer Science Degree',
    'Education',
    'No formal education or a degree in another field than Computer Science.',
    'Ph.D. in Computer Science with an exceptional academic record.'
),
(
    '30b5f7cc-53d8-4d89-b918-3610c9b7439e',
    'Marketing Degree',
    'Education',
    'No formal education or a degree in another field than Marketing.',
    'Ph.D. in Marketing with an exceptional academic record.'
),
-- Work Experience
(
    '6b37f8de-43d8-4c67-b918-7910c9b7435e', 
    'Work Experience (5+ years)',
    'Work Experience',
    'No mention of any work experience or job-related skills.',
    'Extensive work history with at least 5 years of experience in relevant fields.'
),
(
    '6b37f8de-43d8-4c67-b918-7910c9b7430f', 
    'Work Experience (10+ years)',
    'Work Experience',
    'No mention of any work experience or job-related skills.',
    'Exceptional work history with at least 10 years of experience in relevant fields.'
),
-- Languages
(
    'd1e7f5cc-13d8-4a23-b918-2710c9b743ea', 
    'English Proficiency',
    'Language',
    'No mention of English language proficiency.',
    'Fluent in English with strong written and verbal communication skills. Mother tongue or C2 qualification.'
),
(
    'e1e7f5cc-13d8-4a23-b918-2710c9b743ea', 
    'German Proficiency',
    'Language',
    'No mention of German language proficiency.',
    'Fluent in German with strong written and verbal communication skills. Mother tongue or C2 qualification.'
),
-- Frameworks
(
    'e1a7f5cc-13d5-4a23-b918-2710c9b743eb', 
    'Angular',
    'Programming Framework',
    'No mention of experience with Angular framework.',
    'Extensive experience with Angular framework, including complex projects. Demonstrated expertise at the highest level.'
),
(
    'a1a7f5cc-13d5-4a23-b948-2710c9b743eb', 
    'React',
    'Programming Framework',
    'No mention of experience with React framework.',
    'Extensive experience with React framework, including complex projects. Demonstrated expertise at the highest level.'
);


-- Vacancy category links
INSERT INTO vacancy_category (
    vacancy_id,
    category_id,
    weight
) VALUES (
    '6ca830b2-99b5-11ee-b9d1-0242ac120002',
    '025f2219-c03d-48b7-94b9-5c0557e21745',
    50.00
);

INSERT INTO vacancy_category (
    vacancy_id,
    category_id,
    weight
) VALUES (
    '6ca830b2-99b5-11ee-b9d1-0242ac120002',
    '24023f40-023a-4f26-85aa-193b5a0574f1',
    50.00
);

INSERT INTO vacancy_category (
    vacancy_id,
    category_id,
    weight
) VALUES (
    'dae80908-4cce-4d65-9357-ea48f7f2e4af',
    '9d44632c-a079-46bd-9100-09fb9dade3ec',
    50.00
);

INSERT INTO vacancy_category (
    vacancy_id,
    category_id,
    weight
) VALUES (
    'dae80908-4cce-4d65-9357-ea48f7f2e4af',
    '24023f40-023a-4f26-85aa-193b5a0574f1',
    50.00
);

-- Example employees
INSERT INTO employee (
    id,
    first_name,
    last_name,
    email,
    phone_number,
    face_image,
    created_at
) VALUES (
    'f4ebbefa-5c91-4051-ba2e-9ae051d0f481',
    'John',
    'Doe',
    'j.doe@example.com',
    '0612345678',
    NULL,
    CURRENT_TIMESTAMP
);

INSERT INTO employee (
    id,
    first_name,
    last_name,
    email,
    phone_number,
    face_image,
    created_at
) VALUES (
    'a75b1d2d-f9dc-4951-9c80-f81323047c30',
    'Mike',
    'Smith',
    'm.smith@example.com',
    '5626453512',
    NULL,
    CURRENT_TIMESTAMP
);
