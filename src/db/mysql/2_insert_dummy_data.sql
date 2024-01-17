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
) VALUES (
    '9d44632c-a079-46bd-9100-09fb9dade3ec',
    'Java',
    'Programming Language',
    'Does not mention any Java coding related experiences or skills',
    'Highlights extensive coding experiences, showcasing expertise in Java.'
);

INSERT INTO category (
    id,
    name,
    chip,
    guideline_for_zero,
    guideline_for_ten
) VALUES (
    '025f2219-c03d-48b7-94b9-5c0557e21745',
    'Javascript',
    'Programming Language',
    'Does not mention any Javascript coding related experiences or skills',
    'Highlights extensive coding experiences, showcasing expertise in Javascript.'
);

INSERT INTO category (
    id,
    name,
    chip,
    guideline_for_zero,
    guideline_for_ten
) VALUES (
    '24023f40-023a-4f26-85aa-193b5a0574f1',
    'Teamwork',
    'Soft Skills',
    'Does not mention any collaborative projects or teamwork experiences.',
    'Highlights various collaborative projects, demonstrating the ability to work effectively in a team.'
);

-- Vacancy category links
INSERT INTO vacancy_category (
    vacancy_id,
    category_id,
    weight
) VALUES (
    '6ca830b2-99b5-11ee-b9d1-0242ac120002',
    '025f2219-c03d-48b7-94b9-5c0557e21745',
    25.00
);

INSERT INTO vacancy_category (
    vacancy_id,
    category_id,
    weight
) VALUES (
    '6ca830b2-99b5-11ee-b9d1-0242ac120002',
    '24023f40-023a-4f26-85aa-193b5a0574f1',
    25.00
);

INSERT INTO vacancy_category (
    vacancy_id,
    category_id,
    weight
) VALUES (
    'dae80908-4cce-4d65-9357-ea48f7f2e4af',
    '9d44632c-a079-46bd-9100-09fb9dade3ec',
    25.00
);

INSERT INTO vacancy_category (
    vacancy_id,
    category_id,
    weight
) VALUES (
    'dae80908-4cce-4d65-9357-ea48f7f2e4af',
    '24023f40-023a-4f26-85aa-193b5a0574f1',
    25.00
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
