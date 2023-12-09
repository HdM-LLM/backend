from flask import Blueprint, request
from flask_restful import Api, Resource
import services.pdf_service as pdf_service
import services.cv_service as cv_service
import services.rating_service as rating_service
from classes.applicant import Applicant
from classes.cv import CV
from db.mapper.mysql_mapper.applicant_mapper import ApplicantMapper
from db.mapper.mongodb_mapper.cv_mapper import CVMapper
import PyPDF2


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

        cv_pdf_file = request.files['cv']

        cv_content = pdf_service.getPdfContent(cv_pdf_file)

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

        with ApplicantMapper() as applicant_mapper:
            # TODO: Should be changed to get_by_mail when finished with testing
            if applicant_mapper.get_by_id(applicant.get_id()):
                return 'Applicant exists already', 409
            else:
                applicant_mapper.insert(applicant)

                with CVMapper() as cv_mapper:
                    cv_mapper.insert(cv_content, applicant)

                # TODO: Remove the comment if you want to get a rating
                # I commented the line since this is allways an api call ti openai
                # print(rating_service.rate_applicant(applicant))

                return 'Applicant and CV have been saved in database', 200



# Add the resource to the api
api.add_resource(ApplicantResource, '/upload')
