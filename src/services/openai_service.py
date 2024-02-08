"""Module Description: This module contains functions for interacting with the OpenAI API, including loading API keys, executing prompts, and validating responses.

Functions:
    load_dot_env() -> None: Loads the API key from the .env file.
    count_tokens(prompt: str) -> int: Returns the number of tokens in a prompt.
    execute_prompt(prompt: str) -> str: Sends the prompt to the OpenAI model and returns the response.
    validate_response(response: str, required_keys: List[str]) -> bool: Validates if the response is a valid JSON with the given keys.
"""

import openai
import os
from dotenv import load_dotenv
import time
from services.log_service import log
import json
from typing import List

def load_dot_env() -> None:
    """
    Loads the API key from the .env file.
    """
    load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    openai.api_key = OPENAI_API_KEY


def count_tokens(prompt: str) -> int:
    """
    Returns the number of tokens in a prompt.

    Args:
        prompt (str): The prompt to count tokens from.

    Returns:
        int: The number of tokens in the prompt.
    """
    words = prompt.split()
    num_tokens = len(words)
    return num_tokens


def execute_prompt(prompt: str) -> str:
    """
    Sends the prompt to the OpenAI model and returns the response.

    Args:
        prompt (str): The prompt to send to the OpenAI model.

    Returns:
        str: The response from the model.
    """
    truncated_prompt = prompt[:100] + "..." if len(prompt) > 100 else prompt
    num_tokens = count_tokens(prompt)
    print(f"Sending request ({num_tokens} tokens) to GPT-4...")
    log("rating_service", "GPT-4 Request: " + prompt)

    start_time = time.time()
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-1106-preview",
            messages=[
                {
                    "role": "system",
                    "content": "You are a critical Human Resources professional who evaluates job applicants objectively and attentively.",
                },
                {"role": "user", "content": prompt},
            ],            
            temperature = 0.2,
            timeout=200,  # Set the timeout in seconds
            n=1,
        )
        log("rating_service", "GPT-4 Response: " + str(response))
    except openai.error.OpenAIError as e:
        print(f"Error from OpenAI: {e}")
        return "Timeout: No response from OpenAI within the specified time."

    end_time = time.time()

    duration = end_time - start_time
    print(f"Response from GPT-4 received. It took {duration:.2f} seconds.")

    response_string = response.choices[0].message["content"].strip()
    return response_string

def validate_response(response: str, required_keys: List[str]) -> bool:
    """
    Validates if the response is a valid JSON with the given keys.

    Args:
        response (str): The response to be validated.
        required_keys (List[str]): List of required keys in the JSON.

    Returns:
        bool: True if the response is valid, False otherwise.
    """
    try:
        # Attempt to parse the response as JSON
        json_data = json.loads(response)

        # Check if all required keys are present in the JSON
        if all(key in json_data for key in required_keys):
            return True
        else:
            print("Not all required keys present in the JSON.")
            return False

    except json.JSONDecodeError:
        print("Invalid JSON format.")
        return False
