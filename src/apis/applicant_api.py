from uuid import UUID

from flask import Blueprint, request
from flask_restful import Api, Resource
import services.pdf_service as pdf_service
import services.cv_service as cv_service
import services.rating_service as rating_service
from classes.applicant import Applicant
from classes.rating import Rating
from classes.cv import CV
from db.mapper.mysql_mapper.applicant_mapper import ApplicantMapper
from db.mapper.mongodb_mapper.cv_mapper import CVMapper
from db.mapper.mysql_mapper.rating_mapper import RatingMapper
import PyPDF2


# Creates a new blueprint
file_upload = Blueprint('file_upload', __name__)
api = Api(file_upload)


# Class containing all endpoints for applicants
class ApplicantResource(Resource):

    def get(self):
        return 'Hello Upload Page!'

    def post(self):
        """
        Rates and saves an applicant together with the CV
        """
        if 'cv' not in request.files:
            return 'No file part found in POST request.', 400

        cv_pdf_file = request.files['cv']
        cv_content = pdf_service.getPdfContent(cv_pdf_file)

        # Create applicant
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

        # Insert the applicant into the mysql db
        with ApplicantMapper() as applicant_mapper:
            # TODO: Should be changed to get_by_mail when finished with testing
            if applicant_mapper.get_by_id(applicant.get_id()):
                return 'Applicant exists already', 409
            else:
                applicant_mapper.insert(applicant)

        # Create cv
        cv = CV(
            cv_content
        )

        # Insert the cv into the mongodb
        with CVMapper() as cv_mapper:
            cv_mapper.insert(cv, applicant)

        # Get the rating of the categories from the vacancy (OpenAI)
        model_response = rating_service.rate_applicant(applicant)

        # Get the ratings from rhe response
        # TODO: Vacancy is hardcoded at the moment should be changed in future
        ratings = rating_service.create_rating_objects(
            model_response,
            UUID('dae80908-4cce-4d65-9357-ea48f7f2e4af'),
            applicant.get_id()
        )

        # Insert the ratings into the mysql db
        for rating in ratings:
            with RatingMapper() as rating_mapper:
                rating_mapper.insert(rating)


        return 'Applicant, CV and rating have been saved in database', 200



# Add the resource to the api
api.add_resource(ApplicantResource, '/upload')
