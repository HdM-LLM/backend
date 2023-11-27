import os
import openai
from dotenv import load_dotenv
from langchain.llms import OpenAI as LangChainOpenAI
import json
import mysql.connector
import time 
import PyPDF2
import re

class Applicant:
    def __init__(self, first_name, last_name, phone_number, email_address, position):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.email_address = email_address
        self.position = position
        self.ratings_cv = {}

    def update_ratings(self, rating_data):
        for category, details in rating_data.items():
            score = details.get('Score', 0)
            justification = details.get('Justification', '')
            quote = details.get('Quote', '')

            self.ratings_cv[category] = {
                "Score": score,
                "Justification": justification,
                "Quote": quote,
            }

def count_tokens(text):
    # Teile den Text in Wörter und zähle die Token
    words = text.split()
    num_tokens = len(words)
    return num_tokens

def load_openai_model():
    load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    openai.api_key = OPENAI_API_KEY

    class OpenAIModelIO(LangChainOpenAI):
        def query(self, prompt):
            truncated_prompt = prompt[:100] + "..." if len(prompt) > 100 else prompt
            num_tokens = count_tokens(prompt)
            print(f"Die Anfrage hat {num_tokens} Token.")
            print("Prompt an OpenAI: ", {truncated_prompt} )

            start_time = time.time()
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4-1106-preview",
                    messages=[
                        {"role": "system", "content": "You are a critical Human Resources professional who evaluates job applicants objectively and attentively."},
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
            return response.choices[0].message['content'].strip()

    return OpenAIModelIO()

def load_possible_positions(cursor):
    cursor.execute("SELECT position FROM job_postings")
    positions = [row[0] for row in cursor.fetchall()]
    return positions

def load_categories_for_position(cursor, position):
    cursor.execute("""
        SELECT jc.category_name, jc.guideline_0, jc.guideline_10
        FROM job_categories jc
        JOIN job_posting_categories jpc ON jc.id = jpc.category_id
        JOIN job_postings jp ON jpc.job_posting_id = jp.id
        WHERE jp.position = %s
    """, (position,))
    categories = [(row[0], row[1], row[2]) for row in cursor.fetchall()]
    return categories

def create_applicant(data, position):
    return Applicant(data["First Name"], data["Last Name"], data["Phone Number"], data["Email Address"], position)

def create_rating_prompt(categories, text, position):
    rating_prompts = []
    for category, guideline_0, guideline_10 in categories:
        rating_prompts.append(
            f'"{category}": {{"Score": "", "Justification": "", "Quote": "", "Guideline_0": "{guideline_0}", "Guideline_10": "{guideline_10}"}}'
        )

    categories_string = ", ".join(rating_prompts)
    return f"""
    Please rate the following categories from 0 to 10, and provide a justification and a quote from the application for each rating. If you find a category not applicable or impossible to rate, please assign a score of 0 and refrain from providing a written explanation:
    {text}

    Ratings in JSON format:
    {{
        {categories_string}
    }}
    """

def extract_applicant_metadata(openai_model, text):
    prompt_cv_metadata = f"""
    Extract metadata from the curriculum vitae:

    {text}

    Please provide the response in the following JSON format:
    {{
        "First Name": "",
        "Last Name": "",
        "Phone Number": "",
        "Email Address": ""
    }}
    """
    response_cv_metadata = openai_model.query(prompt_cv_metadata)
    # Use regular expression to extract the content between triple backticks
    match = re.search(r'```(.+?)```', response_cv_metadata, re.DOTALL)

    if match:
        # Extract the matched content
        content_between_backticks = match.group(1)
        trimmed_json = content_between_backticks[4:]
        # Replace "N/A" with "0"
        trimmed_json = trimmed_json.replace("N/A", "0")



    data = json.loads(trimmed_json)
    return data

def analyze_application(openai_model, text, position, cursor):
    applicant_metadata = extract_applicant_metadata(openai_model, text)
    applicant = create_applicant(applicant_metadata, position)

    categories = load_categories_for_position(cursor, position)

    rating_prompt = create_rating_prompt(categories, text, position)
    rating_response = openai_model.query(rating_prompt)

        # Use regular expression to extract the content between triple backticks
    match = re.search(r'```(.+?)```', rating_response, re.DOTALL)

    if match:
        # Extract the matched content
        content_between_backticks = match.group(1)
        trimmed_json = content_between_backticks[4:]
        # Replace "N/A" with "0"
        trimmed_json = trimmed_json.replace("N/A", "0")

        rating_data = json.loads(trimmed_json)

        applicant.update_ratings(rating_data)

        return applicant
    else:
        print("ERROR:{rating_response}")
        return None


def insert_applicant_and_ratings_into_database(applicant, cursor):
    # Query to get position_id based on the provided position
    get_position_id_query = "SELECT id FROM job_postings WHERE position = %s"
    cursor.execute(get_position_id_query, (applicant.position,))
    position_row = cursor.fetchone()

    if position_row is not None:
        position_id = position_row[0]

        # Insert basic applicant information
        insert_applicant_query = """
        INSERT INTO applicants (first_name, last_name, phone_number, email_address, position_id, model)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_applicant_query, (applicant.first_name, applicant.last_name, applicant.phone_number, applicant.email_address, position_id, 'gpt-4-1106-preview'))

        # Get the last inserted applicant_id
        applicant_id = cursor.lastrowid

            # Insert ratings information
        for category, details in applicant.ratings_cv.items():
            insert_ratings_query = """
            INSERT INTO applicant_ratings (applicant_id, category, score, justification, quote, model)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_ratings_query, (applicant_id, category, details['Score'], details['Justification'], details['Quote'], 'gpt-4-1106-preview'))


            # Commit the changes to the database
            connection.commit()

        # Print a summary of the applicant
        print("Applicant Summary:")
        print(f"Name: {applicant.first_name} {applicant.last_name}")
        print(f"Phone Number: {applicant.phone_number}")
        print(f"Email Address: {applicant.email_address}")
        print(f"Position: {applicant.position}")

        print("\nRatings:")
        for category, details in applicant.ratings_cv.items():
            print(f"{category}:")
            print(f"  Score: {details['Score']}")
            print(f"  Justification: {details['Justification']}")
            print(f"  Quote: {details['Quote']}")

    else:
        print(f"Error: Position '{applicant.position}' not found in job_postings table.")


def read_pdf(file_path):
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        num_pages = len(pdf_reader.pages)
        text = ""
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
        return text




# Connect to the database
connection = mysql.connector.connect(
    host="127.0.0.1",
    port=3307,
    user="root",
    password="password",
    database="skillsync"
)

# Create a cursor
cursor = connection.cursor()

# Load possible positions from the database (für zukünftiges Automatisches Stellen erkennen anhand des Anschreibens)
#possible_positions = load_possible_positions(cursor)
# Specify the known position
position = "Front End Developer"

# Pfad zur Datei
#file_path_cv = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vector_input_data", "cv_en_martin_marketing.txt")
folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "CVs")


for filename in os.listdir(folder_path):
    if filename.endswith(".pdf"):
        file_path = os.path.join(folder_path, filename)
        #print(f"Reading {filename}:")
        cv = read_pdf(file_path)

    # Überprüfen, ob die Datei existiert
    #if os.path.exists(file_path_cv):
    #    with open(file_path_cv, "r", encoding="utf-8") as file:
    #        cv = file.read().replace('\n', '')

        openai_model = load_openai_model()
        applicant = analyze_application(openai_model, cv, position, cursor)
        if applicant is not None:
            insert_applicant_and_ratings_into_database(applicant, cursor)
        else:
            print("skipped applicant")

        # Close the cursor and connection
        
   # else:
       # print(f"Die Datei {file_path_cv} existiert nicht.")
cursor.close()
connection.close()


