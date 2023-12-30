import PyPDF2
from io import BytesIO


def getPdfContent(pdf_file) -> str:
    """
    Returns the content of a pdf file
    :param pdf_file: pdf file from which the content should be extracted
    :return: Content of the pdf as string
    """
    content = ""

    pdf_reader = PyPDF2.PdfReader(pdf_file)
    num_pages = len(pdf_reader.pages)

    for page_number in range(num_pages):
        page = pdf_reader.pages[page_number]
        content += page.extract_text()

    # Reset the file pointer
    pdf_file.seek(0)

    return content
