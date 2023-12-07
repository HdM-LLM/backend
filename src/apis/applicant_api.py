from flask import Blueprint, request
from flask_restful import Api, Resource
import services.pdf_service as pdf_service
import services.cv_service as cv_service
from classes.applicant import Applicant
from db.mapper.mysql_mapper.applicant_mapper import ApplicantMapper

# Creates a new blueprint
file_upload = Blueprint('file_upload', __name__)
api = Api(file_upload)


# Class containing all endpoints for applicants
class ApplicantResource(Resource):

    def get(self):
        return 'Hello Upload Page!'

    def post(self):
        if 'cv' not in request.files:
            return 'No file part found in POST request.', 400

        pdf_file = request.files['cv']

        cv_content = pdf_service.getPdfContent(pdf_file)

        applicant = Applicant(
            cv_service.get_first_name_from_cv(cv_content),
            cv_service.get_last_name_from_cv(cv_content),
            cv_service.get_date_of_birth_from_cv(cv_content),
            cv_service.get_street_from_cv(cv_content),
            cv_service.get_postal_code_from_cv(cv_content),
            cv_service.get_city_code_from_cv(cv_content),
            cv_service.get_email_from_cv(cv_content),
            cv_service.get_email_from_cv(cv_content),
        )

        with ApplicantMapper() as mapper:
            if mapper.get_by_email(applicant.get_email()):
                return 'Applicant exists already', 409
            else:
                mapper.insert(applicant)
                return 'Applicant has been saved in database', 200


# Add the resource to the api
api.add_resource(ApplicantResource, '/upload')
