import PyPDF2

def getPdfConten(pdf_file):
    content = ""

    pdf_reader = PyPDF2.PdfReader(pdf_file)
    num_pages = len(pdf_reader.pages)

    for page_number in range(num_pages):
        page = pdf_reader.pages[page_number]
        content += page.extract_text()

    return content
