import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import os
import face_recognition


# mac users might want to install tesseract via brew
# 'brew install tesseract' and 'brew install tesseract-lang' (for german)

# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
custom_oem_psm_config = '--oem 3 --psm 1'

# Page segmentation modes (PSM):
#   0    Orientation and script detection (OSD) only.
#   1    Automatic page segmentation with OSD.
#   2    Automatic page segmentation, but no OSD, or OCR. (not implemented)
#   3    Fully automatic page segmentation, but no OSD. (Default)
#   4    Assume a single column of text of variable sizes.
#   5    Assume a single uniform block of vertically aligned text.
#   6    Assume a single uniform block of text.
#   7    Treat the image as a single text line.
#   8    Treat the image as a single word.
#   9    Treat the image as a single word in a circle.
#  10    Treat the image as a single character.
#  11    Sparse text. Find as much text as possible in no particular order.
#  12    Sparse text with OSD.
#  13    Raw line. Treat the image as a single text line, bypassing hacks that are Tesseract-specific.
#
# OCR Engine modes (oem):
#   0    Legacy engine only.
#   1    Neural nets LSTM engine only.
#   2    Legacy + LSTM engines.
#   3    Default, based on what is available.


# NOTE: backend folder acts as root for python
pdf_path = "./src/services/Lebenslauf_TESAT.pdf"
output_directory = "./src/ocr_output"


# Read an image and extract text from it.
def ocr_from_image(image_path: str) -> str:
    image = Image.open(image_path)
    text = pytesseract.image_to_string(
        image, lang='deu')
    return text


# Read a PDF and extract text from it.
def ocr_from_pdf(pdf_path: str, output_folder: str) -> str:
    images = convert_from_path(pdf_path, output_folder=output_folder)
    all_text = ""
    for image in images:
        text = pytesseract.image_to_string(
            image, lang='deu', config=custom_oem_psm_config)
        all_text += text + "\n"
    return all_text


# Extract images from a PDF.
def extract_images_from_pdf(pdf_path: str, output_folder: str) -> list:
    images = convert_from_path(pdf_path)
    extracted_images = []
    for idx, image in enumerate(images):
        output_path = os.path.join(output_folder, f"extracted_image_{idx}.png")
        image.save(output_path, 'PNG')
        extracted_images.append(output_path)
    return extracted_images


# Extract faces from an image.
def extract_faces_from_image(image_path: str, output_folder: str, offset: int = 40) -> list:
    image = face_recognition.load_image_file(image_path)
    face_locations = face_recognition.face_locations(image)

    extracted_faces = []

    # For each face, extract the face and save it as a new image.
    for idx, face_location in enumerate(face_locations):
        top, right, bottom, left = face_location

        # Extend the area around the face.
        top = max(0, top - offset - 80)
        left = max(0, left - offset - 40)
        bottom = min(image.shape[0], bottom + offset)
        right = min(image.shape[1], right + offset + 40)

        # Crop the image and save it as png.
        face_image = Image.open(image_path).crop((left, top, right, bottom))
        output_path = os.path.join(output_folder, f"face_{idx}.png")
        face_image.save(output_path, 'PNG')
        extracted_faces.append(output_path)

    return extracted_faces


# test ocr_from_pdf
print(ocr_from_pdf(pdf_path, output_directory))


# extracted_images = extract_images_from_pdf(pdf_path, output_folder)
# for img_path in extracted_images:
#     print(f"Extrahiertes Bild: {img_path}")
#     extracted_faces = extract_faces_from_image(img_path, output_folder)
#     for face_path in extracted_faces:
#         print(f"Extrahiertes Gesicht: {face_path}")

# print(ocr_from_pdf(pdf_path))
