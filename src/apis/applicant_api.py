from flask import Blueprint, request
from flask_restful import Api, Resource
import os

# Creates a new blueprint
file_upload = Blueprint('file_upload', __name__)
api = Api(file_upload)


# Class containing all endpoints for applicants
class ApplicantResource(Resource):

    def get(self):
        return 'Hello Upload Page!'

    def post(self):
        if 'pdfFile' not in request.files:
            return 'No file part found in POST request.', 400

        pdf_file = request.files['pdfFile']

        # Handle the uploaded file (save, process, etc.)
        print('File name: ' + pdf_file.filename)

        # Change filename to the applicant id
        pdf_file.filename = 'applicant_1234.pdf'

        # Check if the folder exists, if not create it
        if not os.path.exists('./src/apis/uploads'):
            os.makedirs('./src/apis/uploads')

        # Save pdf file to the uploads folder
        pdf_file.save('./src/apis/uploads/' + pdf_file.filename)

        return f"File '{pdf_file.filename}' uploaded successfully.", 200


# Add the resource to the api
api.add_resource(ApplicantResource, '/upload')
