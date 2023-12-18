import os
from typing import List

import openai
from dotenv import load_dotenv, find_dotenv
import time
from db.mapper.mongodb_mapper.vacancy_mapper import VacancyMapper
from db.mapper.mongodb_mapper.cv_mapper import CVMapper
from uuid import UUID
from classes.applicant import Applicant
from classes.rating import Rating
import json


def load_dot_env() -> None:
    """
    Loads the api-key from the .env
    :return: None
    """
    load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    openai.api_key = OPENAI_API_KEY


def count_tokens(prompt) -> int:
    """
    Returns the amount of tokens inside a prompt
    :param prompt: Prompt which should be tokenized
    :return: Amount of tokens
    """
    words = prompt.split()
    num_tokens = len(words)
    return num_tokens


def get_list_of_categories_from_vacancy(vacancy_id: UUID) -> List:
    """
    Returns list of categories of a specific vacancy
    :param vacancy_id: ID of the vacancy of which the categories should be returned
    :return: List of categories
    """
    categories = []

    with VacancyMapper() as vacancy_mapper:
        vacancy = vacancy_mapper.get_by_id(vacancy_id)

    for category in vacancy.get_categories():
        categories.append(category)

    return categories


def get_cv_content_of_applicant(applicant_id: UUID):
    """
    Returns the content of a CV from an applicant from the db
    :param applicant_id: ID of the applicant from whom CV the content should be returned
    :return:
    """

    with CVMapper() as cv_mapper:
        cv_content = cv_mapper.get_by_id(applicant_id)['data'].decode()

    return cv_content


def execute_prompt(prompt):
    """
    Sends the prompt to the OpenAI model
    :param prompt: Prompt which, should be sent to the model
    :return: The response from the model
    """
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
            timeout=200,  # Set the timeout in seconds
            n=1
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
    """
    Creates the prompt for the OpenAI model
    :param categories: Categories, which should be rated from the model
    :param cv_content: Content of the CV, which should be rated
    :return:
    """
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


def rate_applicant(applicant: Applicant, vacancy_id: UUID):
    """
    Puts together the steps to rate an applicant
    :param applicant: Applicant which should be rated
    :return: The rated categories from the model
    """
    # 1. Load the model
    load_dot_env()

    # 2. Get the categories of the vacancy, which will be used for rating
    # TODO: at the moment hard coded to the frontend engineer vacancy uuid
    categories = get_list_of_categories_from_vacancy(vacancy_id)

    # 3. Get the content of the cv pdf
    cv_content = get_cv_content_of_applicant(applicant.get_id())

    # 4. Generate the prompt with both category and cv_content
    prompt = create_rating_prompt(categories, cv_content)

    # 5. Return the response of GPT
    return execute_prompt(prompt)


def extract_ratings_from_response(model_response: str) -> []:
    """
    Extracts the ratings from the response of the OpenAI model
    :param model_response: Response of the OpenAI model
    :return: Lists of categories
    """
    start_index = model_response.find('{')
    end_index = model_response.rfind('}') + 1

    json_block_response = model_response[start_index:end_index]

    parsed_json = json.loads(json_block_response)

    list_of_rating_responses = []

    for category_name in list(parsed_json.keys()):

        category = { category_name : parsed_json[category_name]}

        list_of_rating_responses.append(category)

    return list_of_rating_responses


def create_rating_objects(model_response: str, vacancy_id: UUID, applicant_id: UUID) -> List:
    """
    Creates rating instances
    :param model_response: Response of the OpenAI model
    :param vacancy_id: ID of the vacancy corresponding to the rating
    :param applicant_id: ID of the applicant corresponding to the rating
    :return: List of rating instances
    """
    list_of_rating_responses = extract_ratings_from_response(model_response)
    ratings = []

    with VacancyMapper() as vacancy_mapper:
        vacancy = vacancy_mapper.get_by_id(vacancy_id)

    for rating_response in list_of_rating_responses:
        category_name_response = list(rating_response.keys())[0]
        category_values_response = list(rating_response.values())[0]
        category_id: UUID

        for category in vacancy.get_categories():
            if category.get_name() == category_name_response:
                category_id = category.get_id()

        # Get values with defaults if keys are missing
        score = category_values_response.get('Score', None)
        justification = category_values_response.get('Justification', None)
        quote = category_values_response.get('Quote', None)

        # Check if any required key is missing
        if any(v is None for v in (score, justification, quote)):
            print(f"Warning: Missing key(s) in category '{category_name_response}'")

        rating = Rating(
            category_id,
            vacancy_id,
            applicant_id,
            score,
            justification,
            quote,
        )

        ratings.append(rating)

    return ratings