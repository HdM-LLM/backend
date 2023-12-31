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
from services.log_service import log
from services import openai_service


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


def create_rating_prompt(categories, cv_content):
    """
    Creates the prompt for the OpenAI model
    :param categories: Categories, which should be rated from the model
    :param cv_content: Content of the CV, which should be rated
    :return:
    """
    rating_prompts = []

    for category in categories:
        rating_prompts.append(
            f'"{category.get_name()}": {{"Score": "", "Justification": "", "Quote": "", "Guideline_0": "{category.get_guideline_for_zero()}", "Guideline_10": "{category.get_guideline_for_ten()}"}}'
        )

    categories_string = ", ".join(rating_prompts)

    return f"""
    Please rate the following categories from 0 to 10, and always provide a justification and a quote
    from the application for each rating. If you find a category not applicable or impossible to rate,
    please assign a score of 0, refrain from providing a written explanation and provide an empty quote:
    {cv_content}

    Ratings in JSON format:
    {{
        {categories_string}
    }}
    """


def rate_applicant_and_create_rating_objects(
        cv_content_string: str, applicant: Applicant, vacancy_id: str, try_limit: int = 3) -> List[Rating]:
    """
    Puts together the steps to rate an applicant and create rating objects
    :param cv_content_string: Content of the CV, which should be rated
    :param applicant: Applicant which should be rated
    :param vacancy_id: ID of the vacancy corresponding to the rating
    :return: List of rating objects
    """
    ratings = []
    try_count = 0

    while try_count < try_limit:
        try:
            model_response = rate_applicant(
                cv_content_string, applicant, vacancy_id)
            ratings = create_rating_objects(
                model_response, vacancy_id, applicant.get_id()
            )
            break
        except json.decoder.JSONDecodeError as e:
            print(f"Error while parsing JSON: {e}")
            try_count += 1
            if try_count < try_limit:
                print(f"Retrying ({try_count}/{try_limit})...")
                log("rating_service", "Retrying...")
            else:
                print(f"Error while parsing JSON: {e}")
                log("rating_service", "Error while parsing JSON: " + str(e))
                raise e
    return ratings


def rate_applicant(cv_content_string: str, applicant: Applicant, vacancy_id: str):
    """
    Puts together the steps to rate an applicant
    :param applicant: Applicant which should be rated
    :return: The rated categories from the model
    """
    # 1. Load the model
    openai_service.load_dot_env()

    # 2. Get the categories of the vacancy, which will be used for rating
    categories = get_list_of_categories_from_vacancy(vacancy_id)

    # 3. Get the content of the cv pdf
    cv_content = cv_content_string

    # 4. Generate the prompt with both category and cv_content
    prompt = create_rating_prompt(categories, cv_content)

    # 5. Return the response of GPT
    return openai_service.execute_prompt(prompt)


def extract_ratings_from_response(model_response: str) -> []:
    """
    Extracts the ratings from the response of the OpenAI model
    :param model_response: Response of the OpenAI model
    :return: Lists of categories
    """
    # TODO: This could be prone to errors if the response changes (unlikely) or if the response is not valid JSON (more likely) -> Error handling (Raise exception?)
    start_index = model_response.find("{")
    end_index = model_response.rfind("}") + 1

    json_block_response = model_response[start_index:end_index]

    # GPT-4 sometimes returns invalid JSON. The exception is caught at a higher level.
    parsed_json = json.loads(json_block_response)

    list_of_rating_responses = []

    for category_name in list(parsed_json.keys()):
        category = {category_name: parsed_json[category_name]}

        list_of_rating_responses.append(category)

    return list_of_rating_responses


def create_rating_objects(
    model_response: str, vacancy_id: UUID, applicant_id: UUID
) -> List:
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
        score = category_values_response.get("Score", None)
        justification = category_values_response.get("Justification", None)
        quote = category_values_response.get("Quote", None)

        # Check if any required key is missing
        if any(v is None for v in (score, justification, quote)):
            print(
                f"Warning: Missing key(s) in category '{category_name_response}'")

        # TODO: Check if quote is in cv before inserting it

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
