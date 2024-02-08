"""Module Description: This module contains functions for extracting personal data from a curriculum vitae (CV) content and processing CV images.

Functions:
    get_personal_data_from_cv(cv_content: str) -> dict: Extracts metadata from the curriculum vitae content provided.
    parse_date_of_birth(date_string: str) -> date: Parses the date of birth from a given string.
    process_cv_image(cv_pdf_file: BinaryIO) -> bytes: Processes the CV image extracted from a PDF file.
    extract_image_from_pdf(pdf_content: bytes) -> bytes: Extracts the image from the PDF content.
    extract_face_from_image(image_content: BytesIO, offset: int = 40) -> bytes: Extracts the face from the image content provided.
    image_to_bytes(image: Image) -> bytes: Converts an image to bytes.
"""

from datetime import datetime, date
import services.openai_service as openai_service
import json
from db.mapper.mysql_mapper.applicant_mapper import ApplicantMapper
from PIL import Image
from io import BytesIO
import face_recognition
from pdf2image import convert_from_bytes
from services.log_service import log

def get_personal_data_from_cv(cv_content: str) -> dict:
    """Extracts metadata from the curriculum vitae content provided.

    Args:
        cv_content (str): The content of the curriculum vitae.

    Returns:
        dict: A dictionary containing the extracted personal data.

    Example:
        >>> get_personal_data_from_cv("CV content...")
        {'first_name': 'John', 'last_name': 'Doe', 'date_of_birth': datetime.date(1990, 5, 15), 'street': '123 Main St', 'postal_code': '12345', 'city': 'City', 'email': 'john.doe@example.com', 'phone_number': '123-456-7890'}
    """
    openai_service.load_dot_env()

    prompt = f"""
    Extract metadata from the curriculum vitae:

    {cv_content}

    Please provide the response in the following JSON format:
    {{
        "first_name": "",
        "last_name": "",
        "date_of_birth": "%D-%M-%Y",
        "street": "",
        "postal_code": "",
        "city": "",
        "email": "",
        "phone_number": ""
    }}

    If you can't find a value, please leave it empty
    """
    log("cv_service", "GPT-4 Request: " + prompt)
    model_response = openai_service.execute_prompt(prompt)
    log("cv_service", "GPT-4 Response: " + model_response)

    start_index = model_response.find('{')
    end_index = model_response.rfind('}') + 1

    json_block_response = model_response[start_index:end_index]

    parsed_json = json.loads(json_block_response)

    parsed_json["date_of_birth"] = parse_date_of_birth(
        parsed_json["date_of_birth"])

    return parsed_json

def parse_date_of_birth(date_string: str) -> date:
    """Parses the date of birth from a given string.

    Args:
        date_string (str): The date of birth string to be parsed.

    Returns:
        date: The parsed date of birth.

    Raises:
        ValueError: If the date string cannot be parsed with the available formats.
    """
    formats_to_try = ["%d.%m.%Y", "%d-%m-%Y"]

    for date_format in formats_to_try:
        try:
            return datetime.strptime(date_string, date_format).date()
        except ValueError:
            pass

    # If none of the formats match
    raise ValueError(f"Could not parse date: {date_string}")

def process_cv_image(cv_pdf_file: BinaryIO) -> bytes:
    """Processes the CV image extracted from a PDF file.

    Args:
        cv_pdf_file (BinaryIO): The PDF file containing the CV.

    Returns:
        bytes: The processed CV image as bytes.
    """
    cv_content = cv_pdf_file.read()

    # Reset the file pointer
    cv_pdf_file.seek(0)

    extracted_face_bytes = extract_image_from_pdf(cv_content)

    return extracted_face_bytes

def extract_image_from_pdf(pdf_content: bytes) -> bytes:
    """Extracts the image from the PDF content.

    Args:
        pdf_content (bytes): The content of the PDF file.

    Returns:
        bytes: The extracted image content as bytes.
    """
    images = convert_from_bytes(pdf_content)

    if not images:
        return None

    # Take only the first image from the PDF
    image = images[0]
    image_content = BytesIO()
    image.save(image_content, 'PNG')
    image_content.seek(0)

    face_image_bytes = extract_face_from_image(image_content)

    return face_image_bytes

def extract_face_from_image(image_content: BytesIO, offset: int = 40) -> bytes:
    """Extracts the face from the image content provided.

    Args:
        image_content (BytesIO): The content of the image.
        offset (int, optional): The offset to expand the face area. Defaults to 40.

    Returns:
        bytes: The extracted face image content as bytes.
    """
    image = face_recognition.load_image_file(image_content)
    face_locations = face_recognition.face_locations(image)

    if not face_locations:
        return None

    top, right, bottom, left = face_locations[0]

    # Extend the area around the face
    top = max(0, top - offset - 80)
    left = max(0, left - offset - 40)
    bottom = min(image.shape[0], bottom + offset)
    right = min(image.shape[1], right + offset + 40)

    face_image = Image.fromarray(image[top:bottom, left:right])

    # Convert the face image to bytes
    face_image_bytes = image_to_bytes(face_image)

    return face_image_bytes

def image_to_bytes(image: Image) -> bytes:
    """Converts an image to bytes.

    Args:
        image (Image): The image to be converted.

    Returns:
        bytes: The image content as bytes.
    """
    image_bytes = BytesIO()
    image.save(image_bytes, format='PNG')
    image_bytes.seek(0)
    return image_bytes.read()
