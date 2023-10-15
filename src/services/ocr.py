import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import os
import face_recognition

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
custom_oem_psm_config = r'--tessdata-dir "C:\Program Files\Tesseract-OCR\tessdata"'

def ocr_from_image(image_path): 
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, lang='deu', config=custom_oem_psm_config)
    return text

def ocr_from_pdf(pdf_path):
    images = convert_from_path(pdf_path)
    all_text = ""
    for image in images:
        text = pytesseract.image_to_string(image, lang='deu')
        all_text += text + "\n"
    return all_text

def extract_images_from_pdf(pdf_path, output_folder):
    images = convert_from_path(pdf_path)
    extracted_images = []
    for idx, image in enumerate(images):
        output_path = os.path.join(output_folder, f"extracted_image_{idx}.png")
        image.save(output_path, 'PNG')
        extracted_images.append(output_path)
    return extracted_images

def extract_faces_from_image(image_path, output_folder, offset=40):
    image = face_recognition.load_image_file(image_path)
    face_locations = face_recognition.face_locations(image)

    extracted_faces = []

    for idx, face_location in enumerate(face_locations):
        top, right, bottom, left = face_location

        # Erweiterung des Bereichs um das Gesicht
        top = max(0, top - offset- 80)
        left = max(0, left - offset - 40)
        bottom = min(image.shape[0], bottom + offset )
        right = min(image.shape[1], right + offset + 40)

        face_image = Image.open(image_path).crop((left, top, right, bottom))
        output_path = os.path.join(output_folder, f"face_{idx}.png")
        face_image.save(output_path, 'PNG')
        extracted_faces.append(output_path)

    return extracted_faces


# Beispiel:
pdf_path = r""
output_folder = r""

extracted_images = extract_images_from_pdf(pdf_path, output_folder)
for img_path in extracted_images:
    print(f"Extrahiertes Bild: {img_path}")
    extracted_faces = extract_faces_from_image(img_path, output_folder)
    for face_path in extracted_faces:
        print(f"Extrahiertes Gesicht: {face_path}")

print(ocr_from_pdf(pdf_path))