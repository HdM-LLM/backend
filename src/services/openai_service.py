import openai
import os
from dotenv import load_dotenv
import time
from services.log_service import log
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


def execute_prompt(prompt):
    """
    Sends the prompt to the OpenAI model
    :param prompt: Prompt which, should be sent to the model
    :return: The response from the model
    """
    truncated_prompt = prompt[:100] + "..." if len(prompt) > 100 else prompt
    num_tokens = count_tokens(prompt)
    # print(f"Die Anfrage hat {num_tokens} Token.")
    # print("Prompt an OpenAI: ", {truncated_prompt})
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

def validate_response(response, required_keys):
    """
    Validates if the response is a valid JSON with the given keys
    :param response: The response to be validated
    :param required_keys: List of required keys in the JSON
    :return: True if the response is valid, False otherwise
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
    