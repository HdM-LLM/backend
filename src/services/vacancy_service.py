from datetime import datetime, date
import services.rating_service as rating_service
import json
from io import BytesIO
import services.openai_service as openai_service

def generate_text(basic_information, selected_categories, adjust_prompt):

    title = basic_information['title']
    department = basic_information['department']
    tasks_and_responsibilities = basic_information['tasksAndResponsibilities']
    working_hours = basic_information['workingHours']
    description = basic_information['description']

    # Create the JSON structure
    full_json_structure = {
        "title": "",
        "department": "",
        "workplace_and_working_hours": "",
        "language_requirements": "",
        "description": "",
    }

     # Extract the required keys from the full_json_structure
    required_keys = list(full_json_structure.keys())

    # Convert the JSON structure to a string
    full_json_structure_str = json.dumps(full_json_structure)


    openai_service.load_dot_env()

    prompt = f"Create a profession vacancy text for the position of {title} in the {department} department. Therse are some basic informations:\n\n"\
         f"**Job Title:** {title}\n"\
         f"**Department:** {department}\n"\
         f"**Tasks and Responsibilities:** {tasks_and_responsibilities}\n"\
         f"**Working Hours:** {working_hours}\n"\
         f"**Description:** {description}\n\n"\
         f"For this position, we are particularly interested in candidates with expertise in the following key skills. Ensure that the generated text provides appealing descriptions for each skill:\n"

    for category in selected_categories:
        skill_name = category['name']
        skill_chip = category['chip']

        prompt += f"\n- **{skill_name}:**\n"\
                f"  Craft an engaging description highlighting the importance of {skill_name} for this role. Emphasize the significance of {skill_name} in {department} and its impact on the success of our projects. Showcase the value of {skill_name} proficiency in {skill_chip} and illustrate how candidates with expertise in {skill_name} contribute to innovation and success within our team.\n"

    prompt += adjust_prompt
    # Closing statement
    prompt += f"\nPlease provide the response in the following JSON format:\n{{\n{full_json_structure_str}\n}}"

    # Attempt to execute the prompt up to 3 times
    for attempt in range(3):
        model_response = openai_service.execute_prompt(prompt)
        start_index = model_response.find('{')
        end_index = model_response.rfind('}') + 1

        json_block_str = model_response[start_index:end_index]

        # Check if the response is a valid JSON with the required keys
        if openai_service.validate_response(json_block_str, required_keys):
            break
        else:
            print(f"Attempt {attempt + 1} failed. Retrying...")
    else:
        # If all attempts fail, raise an error
        raise ValueError("Failed to get a valid response from the model after 3 attempts.")


   

    # Preprocess the JSON string to remove control characters
    json_block_str_cleaned = ''.join(char for char in json_block_str if char.isprintable())

    # Load the cleaned JSON string
    json_block_response = json.loads(json_block_str_cleaned)

    # Create the full text
    full_text_dict = {
    "vacancy_text": f'''
    Job Title: {basic_information['title']}
    Department: {basic_information['department']}
    
    Tasks and Resposibilities:
    {basic_information['tasksAndResponsibilities']}
        
    Workplace and Working Hours:
    {json_block_response['workplace_and_working_hours']}
        
    Description:
    {basic_information['description']}
    '''
    }

    # Convert the dictionary to JSON
    json_data = json.dumps(full_text_dict)
    parsed_json = json.loads(json_data)

    return parsed_json




