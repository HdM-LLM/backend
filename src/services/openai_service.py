import openai
import os
from dotenv import load_dotenv, find_dotenv
import time


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