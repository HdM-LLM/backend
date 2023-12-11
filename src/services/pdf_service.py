import PyPDF2
from io import BytesIO

def getPdfContent(pdf_file):
    """
    Returns the content of a pdf file
    :param pdf_file: pdf file from which the content should be extracted
    :return: Content of the pdf
    """
    content = ""

    pdf_reader = PyPDF2.PdfReader(pdf_file)
    num_pages = len(pdf_reader.pages)

    for page_number in range(num_pages):
        page = pdf_reader.pages[page_number]
        content += page.extract_text()

    return content

