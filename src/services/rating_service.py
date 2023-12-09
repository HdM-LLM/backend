import os
import openai
from dotenv import load_dotenv, find_dotenv
import time
from db.mapper.mongodb_mapper.vacancy_mapper import VacancyMapper
from db.mapper.mongodb_mapper.cv_mapper import CVMapper
from uuid import UUID
from classes.applicant import Applicant


def load_openai_model():
    load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    openai.api_key = OPENAI_API_KEY


def count_tokens(prompt):
    words = prompt.split()
    num_tokens = len(words)
    return num_tokens


def get_list_of_categories_from_vacancy(vacancy_id: UUID):
    categories = []

    vacancy_mapper = VacancyMapper()

    vacancy = vacancy_mapper.get_by_id(vacancy_id)

    for category in vacancy.get_categories():
        categories.append(category)

    return categories


def get_cv_content_of_applicant(applicant_id: UUID):
    cv_mapper = CVMapper()

    cv_content = cv_mapper.get_by_id(applicant_id)['data'].decode()


    return cv_content


def execute_prompt(prompt):
    truncated_prompt = prompt[:100] + "..." if len(prompt) > 100 else prompt
    num_tokens = count_tokens(prompt)
    print(f"Die Anfrage hat {num_tokens} Token.")
    print("Prompt an OpenAI: ", {truncated_prompt})

    start_time = time.time()
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-1106-preview",
            messages=[
                {"role": "system",
                 "content": "You are a critical Human Resources professional who evaluates job applicants objectively and attentively."},
                {"role": "user", "content": prompt}
            ],
            timeout=200  # Set the timeout in seconds
        )
    except openai.error.OpenAIError as e:
        print(f"Error from OpenAI: {e}")
        return "Timeout: No response from OpenAI within the specified time."

    end_time = time.time()

    duration = end_time - start_time
    print(f"Antwort von OpenAI erhalten (Dauer: {duration:.2f} Sekunden)")
    print(response.choices[0].message['content'].strip())
    return response.choices[0].message['content'].strip()


def create_rating_prompt(categories, cv_content):
    rating_prompts = []

    for category in categories:
        rating_prompts.append(f'"{category.get_name()}": {{"Score": "", "Justification": "", "Quote": "", "Guideline_0": "{category.get_guideline_for_zero()}", "Guideline_10": "{category.get_guideline_for_ten()}"}}')

    categories_string = ", ".join(rating_prompts)

    return f"""
    Please rate the following categories from 0 to 10, and provide a justification and a quote
    from the application for each rating. If you find a category not applicable or impossible to rate,
    please assign a score of 0 and refrain from providing a written explanation:
    {cv_content}

    Ratings in JSON format:
    {{
        {categories_string}
    }}
    """


def rate_applicant(applicant: Applicant):
    # 1. Load the model
    load_openai_model()

    # 2. Get the categories of the vacancy, which will be used for rating
    # TODO: at the moment hard coded to the frontend engineer vacancy uuid
    categories = get_list_of_categories_from_vacancy(UUID('dae80908-4cce-4d65-9357-ea48f7f2e4af'))

    # 3. Get the content of the cv pdf
    cv_content = get_cv_content_of_applicant(applicant.get_id())

    # 4. Generate the prompt with both category and cv_content
    prompt = create_rating_prompt(categories, cv_content)

    # 5. Return the response of GPT
    return execute_prompt(prompt)



