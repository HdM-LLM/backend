from datetime import datetime, date
import services.rating_service as rating_service
import json
from io import BytesIO
import services.openai_service as openai_service
from db.mapper.mysql_mapper.category_mapper import CategoryMapper

def trim_to_255(text):
    # Trims the text to 255 characters
    return text[:255]

def get_guidelines(category_name):
    openai_service.load_dot_env()

    prompt = f"""
    Please provide a rating guideline tailored for Human Resources (HR) to evaluate CVs in the {category_name}
    category. The rating guideline should cover a scale from 0 points (the lowest possible) to 10 points 
    (the highest possible). The guideline should focus on the qualifications of the contestant and the skills 
    mentioned in their CV. Please dont make each guideline longer then varchar(200).


    Please provide the response in the following JSON format:
    {{
        "guideline_for_zero": "",
        "guideline_for_ten": "",
    }}
    """

    
    model_response = openai_service.execute_prompt(prompt)

    start_index = model_response.find('{')
    end_index = model_response.rfind('}') + 1

    json_block_response = model_response[start_index:end_index]

    parsed_json = json.loads(json_block_response)

    for key, value in parsed_json.items():
        parsed_json[key] = trim_to_255(value)
        
    return parsed_json




def assign_chip(category_name):
    with CategoryMapper() as mapper:
        distinct_chips = mapper.get_distinct_chips()

    openai_service.load_dot_env()

    prompt = f"""
    Check if a category from this List:

    {distinct_chips}

    Fits to this topic: 

    {category_name}

    else provide me a fitting category name.

    Please provide the response in the following JSON format:
    {{
        "category": "",
        "existed": "true/false",
    }}
    """
    model_response = openai_service.execute_prompt(prompt)

    start_index = model_response.find('{')
    end_index = model_response.rfind('}') + 1

    json_block_response = model_response[start_index:end_index]

    parsed_json = json.loads(json_block_response)

    return parsed_json