db.createCollection("vacancies");


db.vacancies.insertOne({
  uuid: "dae80908-4cce-4d65-9357-ea48f7f2e4af",
  creation_date: "2020-05-17 12:12:12",
  name: "Frontend Engineer",
  description: "Content of the vacancy...",
  department: "Development",
  categories: [
    {
      uuid: "9d44632c-a079-46bd-9100-09fb9dade3ec",
      name: "Coding Skills",
      guideline_0: "Does not mention any coding-related experiences or skills.",
      guideline_10:
        "Highlights extensive coding experiences, showcasing expertise in languages like Python and Java.",
    },
    {
      uuid: "025f2219-c03d-48b7-94b9-5c0557e21745",
      name: "Communication Skills",
      guideline_0:
        "Lacks examples of clear and concise communication in professional contexts.",
      guideline_10:
        "Provides multiple instances of clear and effective communication in professional contexts.",
    },
    {
      uuid: "24023f40-023a-4f26-85aa-193b5a0574f1",
      name: "Teamwork",
      guideline_0:
        "Does not mention any collaborative projects or teamwork experiences.",
      guideline_10:
        "Highlights various collaborative projects, demonstrating the ability to work effectively in a team.",
    },
    {
      uuid: "26ceacd9-0b75-4962-93f2-81dc43f0de85",
      name: "Networking Expertise",
      guideline_0:
        "Does not mention any experiences related to networking concepts or projects.",
      guideline_10:
        "Provides detailed experiences and achievements in networking, showcasing in-depth knowledge.",
    },
    {
      uuid: "70d03b6f-f014-4ec3-a73b-1d81d8c0f4fb",
      name: "Problem-Solving",
      guideline_0:
        "Does not mention any experiences where problem-solving was essential.",
      guideline_10:
        "Highlights various instances where problem-solving skills were crucial, providing detailed examples.",
    },
  ],
});
