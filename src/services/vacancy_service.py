from datetime import datetime, date
import services.rating_service as rating_service
import json
from io import BytesIO
import services.openai_service as openai_service


def generate_text(basic_information, selected_categories, adjust_prompt):

    job_name = basic_information['jobName']
    department = basic_information['department']
    tasks_and_responsibilities = basic_information['tasksAndResponsibilities']
    required_skills = basic_information['requiredSkills']
    workplace_and_working_hours = basic_information['workplaceAndWorkingHours']
    language_requirements = basic_information['languageRequirements']
    additional_information = basic_information['additionalInformation']


    openai_service.load_dot_env()

    prompt = f"Create a profession vacancy text for the position of {job_name} in the {department} department. Include the following details:\n\n"\
         f"**Job Title:** {job_name}\n"\
         f"**Department:** {department}\n"\
         f"**Tasks and Responsibilities:** {tasks_and_responsibilities}\n"\
         f"**Required Skills:** {required_skills}\n"\
         f"**Workplace and Working Hours:** {workplace_and_working_hours}\n"\
         f"**Language Requirements:** {language_requirements}\n"\
         f"**Additional Information:** {additional_information}\n\n"\
         f"For this position, we are particularly interested in candidates with expertise in the following key skills. Ensure that the generated text provides appealing descriptions for each skill:\n"

    for category in selected_categories:
        skill_name = category['name']
        skill_weight = category['weight']
        skill_chip = category['chip']

        prompt += f"\n- **{skill_name}:**\n"\
                f"  Craft an engaging description highlighting the importance of {skill_name} for this role. Emphasize the significance of {skill_name} in {department} and its impact on the success of our projects. Showcase the value of {skill_name} proficiency in {skill_chip} and illustrate how candidates with expertise in {skill_name} contribute to innovation and success within our team.\n"

    prompt += adjust_prompt
    # Closing statement
    prompt += """ Please provide the response in a valid JSON format, and dont use markdown-style formatting in the JSON string. The JSON should only contain plain text an only one key called vacancy_test.
        """

    
    model_response = openai_service.execute_prompt(prompt)

    start_index = model_response.find('{')
    end_index = model_response.rfind('}') + 1

    json_block_response = model_response[start_index:end_index]

    json_data = json.dumps(json_block_response)

    parsed_json = json.loads(json_data)
    print(parsed_json)
    return parsed_json




