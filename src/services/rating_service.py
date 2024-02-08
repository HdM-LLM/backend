"""
Module for rating applicants based on CV content against job vacancies.

Functions:
    get_list_of_categories_from_vacancy(vacancy_id: UUID) -> List: Returns categories of a vacancy.
    create_rating_prompt(categories, cv_content): Creates OpenAI prompt for rating.
    rate_applicant_and_create_rating_objects(cv_content_string: str, applicant: Applicant, vacancy_id: str, try_limit: int = 3) -> List[Rating]: Rates applicant and creates rating objects.
    rate_applicant(cv_content_string: str, applicant: Applicant, vacancy_id: str): Rates an applicant.
    evaluate_model_response(model_response, prompt, applicant_id): Evaluates model response and stores it.
    create_evaluation_prompt(model_response: str, original_prompt: str): Creates prompt for evaluating response.
    extract_ratings_from_response(model_response: str) -> []: Extracts ratings from OpenAI response.
    validate_quote(quote, cv_content): Validates quote presence in CV content.
    create_rating_objects(model_response: str, vacancy_id: UUID, applicant_id: UUID, cv_content_string: str) -> List: Creates rating instances.
"""
import os
from typing import List
import openai
from dotenv import load_dotenv, find_dotenv
import time
from db.mapper.mysql_mapper.vacancy_mapper import VacancyMapper
from db.mapper.mysql_mapper.evaluation_mapper import EvaluationMapper
from db.mapper.mongodb_mapper.cv_mapper import CVMapper
from uuid import UUID
from classes.applicant import Applicant
from classes.rating import Rating
import json
from services.log_service import log
from services import openai_service
import re

def get_list_of_categories_from_vacancy(vacancy_id: UUID) -> List:
    """
    Returns list of categories of a specific vacancy
    :param vacancy_id: ID of the vacancy of which the categories should be returned
    :return: List of categories
    """

    with VacancyMapper() as vacancy_mapper:
        categories_of_vacancy = vacancy_mapper.get_all_categories_by_vacancy_id(vacancy_id)

    return categories_of_vacancy

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
                model_response, vacancy_id, applicant.get_id(), cv_content_string
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
    model_response = openai_service.execute_prompt(prompt)

    # 6. Evaluate the model answer
    evaluate_model_response(model_response, prompt, applicant.get_id())

    return model_response

def evaluate_model_response(model_response, prompt, applicant_id):
    """
    Evaluates the model response and stores the evaluation score in the database.

    :param model_response: The response of the OpenAI model.
    :param prompt: The original prompt used for generating the model response.
    :param applicant_id: The ID of the applicant corresponding to the model response.
    """

     # Check if the 'evaluate_model' environment variable is set
    evaluate_model = os.getenv("evaluate_model")
    if evaluate_model:
        evaluation_prompt = create_evaluation_prompt(model_response, prompt)
        evaluation_score = openai_service.execute_prompt(evaluation_prompt)
        with EvaluationMapper() as evaluation_mapper:
            evaluation_mapper.insert(str(applicant_id), evaluation_score)


def create_evaluation_prompt(model_response: str, original_prompt: str):
    prompt = f"Please rate the model response on a scale of 0-10, based on the task: {original_prompt}"
    prompt += f"The response to the task was: {model_response}"
    prompt += f".Please answer your rating to that response only with a number from 0-10"
    return prompt


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

def validate_quote(quote, cv_content):
    # Normalize the overall CV content for comparison
    normalized_cv_content = ' '.join(cv_content.split()).lower()

    # Check if the quote is empty
    if not quote.strip():
        return "No quote available."

    # Use a regular expression to split the quote by '. ' or '...'
    quote_segments = re.split(r'\.\.\.|\.\s', quote)

    # Normalize segments
    normalized_segments = [' '.join(segment.split()).lower() for segment in quote_segments]

    # Check if all segments are present in the CV content
    if all(segment in normalized_cv_content for segment in normalized_segments if segment):
        return quote
    else:
        return "No quote available."
    
def create_rating_objects(model_response: str, vacancy_id: UUID, applicant_id: UUID, cv_content_string: str) -> List:
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
        vacancy.set_categories(vacancy_mapper.get_all_categories_by_vacancy_id(vacancy_id))

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
        # Check if quote is present in the CV content
        quote = validate_quote(quote, cv_content_string)

        # Check if any required key is missing
        if any(v is None for v in (score, justification, quote)):
            print(
                f"Warning: Missing key(s) in category '{category_name_response}'")

        with VacancyMapper() as vacancy_mapper:
            # Get the weight for the category
            weight = vacancy_mapper.get_weight_by_vacancy_category_ids(vacancy_id,category_id)

        rating = Rating(
            category_id,
            vacancy_id,
            applicant_id,
            score,
            justification,
            quote,
            weight,
        )

        ratings.append(rating)

    return ratings
