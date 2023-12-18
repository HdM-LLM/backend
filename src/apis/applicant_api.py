from flask import Blueprint, request, jsonify
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
import base64
from uuid import UUID


# Creates a new blueprint for upload
file_upload = Blueprint('file_upload', __name__)
api_upload = Api(file_upload)


# Creates a new blueprint for listing applicants
applicant_list = Blueprint('applicant_list', __name__)
api_list = Api(applicant_list)



# Class containing endpoints for /applicants/<string:vacancy_id>
class ApplicantListResource(Resource):

    def get(self, vacancy_id=None):
        with ApplicantMapper() as applicant_mapper:
            if vacancy_id:
                # Fetch applicants by vacancy_id
                applicants_data = applicant_mapper.get_by_vacancy_id(vacancy_id)
            else:
                # Fetch all applicants
                applicants_data = applicant_mapper.get_all()

        formatted_applicants = [
            {
                "id": applicant.get_id(),
                "firstName": applicant.get_first_name(),
                "lastName": applicant.get_last_name(),
                "img":  self.encode_image(applicant.get_face_image()),
                "rating": 2,
                "skills": []
                # Add other data you want to display
            }
            for applicant in applicants_data
        ]

        return jsonify(formatted_applicants)

    def encode_image(self, image_data):
        if image_data is not None:
            return base64.b64encode(image_data).decode('utf-8')
        else:
            return None



# Class containing endpoints for /upload
class ApplicantUploadResource(Resource):

    def post(self):
        if 'cv' not in request.files or 'vacancy' not in request.form:
            return 'Required data not found in POST request.', 400

        cv_pdf_file = request.files['cv']
        vacancy = request.form['vacancy']

        applicant_face_image = cv_service.process_cv_image(cv_pdf_file)

        cv_content = pdf_service.getPdfContent(cv_pdf_file)
        personal_data = cv_service.get_personal_data_from_cv(cv_content)

        applicant = Applicant(
            first_name=personal_data["first_name"],
            last_name=personal_data["last_name"],
            date_of_birth=personal_data["date_of_birth"],
            street=personal_data["street"],
            postal_code=personal_data["postal_code"],
            city=personal_data["city"],
            email=personal_data["email"],
            phone_number=personal_data["phone_number"],
            face_image=applicant_face_image
        )

        with ApplicantMapper() as applicant_mapper:
            if applicant_mapper.get_by_id(applicant.get_id()):
                return 'Applicant exists already', 409
            else:
                applicant_mapper.insert(applicant, vacancy)

        cv = CV(cv_content)

        cv_mapper = CVMapper()
        cv_mapper.insert(cv, applicant)

        model_response = rating_service.rate_applicant(applicant, vacancy)

        ratings = rating_service.create_rating_objects(
            model_response,
            UUID(vacancy),
            applicant.get_id()
        )

        for rating in ratings:
            with RatingMapper() as rating_mapper:
                rating_mapper.insert(rating)

        return 'Applicant, CV, and rating have been saved in the database', 200


# Add the resources to the API with different endpoints
api_list.add_resource(ApplicantListResource, '/applicants', '/applicants/<string:vacancy_id>')
api_upload.add_resource(ApplicantUploadResource, '/upload')
