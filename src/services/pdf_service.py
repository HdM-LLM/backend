"""Module Description: This module contains a function for extracting the content of a PDF file.

Functions:
    getPdfContent(pdf_file) -> str: Returns the content of a PDF file as a string.

"""

import PyPDF2
from io import BytesIO

def getPdfContent(pdf_file) -> str:
    """
    Returns the content of a PDF file as a string.
    
    Args:
        pdf_file: PDF file object or bytes-like object containing the PDF content.
        
    Returns:
        str: Content of the PDF as a string.
    """
    content = ""

    pdf_reader = PyPDF2.PdfReader(pdf_file)
    num_pages = len(pdf_reader.pages)

    for page_number in range(num_pages):
        page = pdf_reader.pages[page_number]
        content += page.extract_text()

    # Reset the file pointer
    if isinstance(pdf_file, BytesIO):
        pdf_file.seek(0)

    return content
