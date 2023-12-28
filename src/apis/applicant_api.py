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
api = Api(applicant_list)


# Class containing endpoints for /applicants
class ApplicantListResource(Resource):

    def encode_image(self, image_data):
        if image_data is not None:
            return base64.b64encode(image_data).decode('utf-8')
        else:
            return None

    # Get all applicants
    def get(self):
        with ApplicantMapper() as mapper:
            applicants = mapper.get_all()

            formatted_applicants = [
                {
                    "id": applicant.get_id(),
                    "firstName": applicant.get_first_name(),
                    "lastName": applicant.get_last_name(),
                    "img": self.encode_image(applicant.get_face_image()),
                    "date_of_birth": applicant.get_date_of_birth(),
                    "street": applicant.get_street(),
                    "postal_code": applicant.get_postal_code(),
                    "city": applicant.get_city(),
                    "email": applicant.get_email(),
                    "phone_number": applicant.get_phone_number(),
                }
                for applicant in applicants
            ]

        return jsonify(formatted_applicants)


# Class containing endpoints to get all applicants by vacancy id
class ApplicantsByVacancyResource(Resource):

    def encode_image(self, image_data):
        if image_data is not None:
            return base64.b64encode(image_data).decode('utf-8')
        else:
            return None

    # Get all applicants by vacancy id
    def get(self, vacancy_id):
        with ApplicantMapper() as mapper:
            applicants = mapper.get_by_vacancy_id(vacancy_id)

            formatted_applicants = [
                {
                    "id": applicant.get_id(),
                    "firstName": applicant.get_first_name(),
                    "lastName": applicant.get_last_name(),
                    "img": self.encode_image(applicant.get_face_image()),
                    "date_of_birth": applicant.get_date_of_birth(),
                    "street": applicant.get_street(),
                    "postal_code": applicant.get_postal_code(),
                    "city": applicant.get_city(),
                    "email": applicant.get_email(),
                    "phone_number": applicant.get_phone_number(),
                }
                for applicant in applicants
            ]

        return jsonify(formatted_applicants)


# Class containing endpoints for handling a single applicant
class ApplicantResource(Resource):
    def encode_image(self, image_data):
        if image_data is not None:
            return base64.b64encode(image_data).decode('utf-8')
        else:
            return None

    # Get one applicant by id
    def get(self, applicant_id):
        if applicant_id is None:
            return None

        with ApplicantMapper() as mapper:
            applicant = mapper.get_by_id(applicant_id)

            formatted_applicant = {
                "id": applicant.get_id(),
                "firstName": applicant.get_first_name(),
                "lastName": applicant.get_last_name(),
                "img":  self.encode_image(applicant.get_face_image()),
                "date_of_birth": applicant.get_date_of_birth(),
                "street": applicant.get_street(),
                "postal_code": applicant.get_postal_code(),
                "city": applicant.get_city(),
                "email": applicant.get_email(),
                "phone_number": applicant.get_phone_number(),
            }

        return jsonify(formatted_applicant)


class ApplicantCVResource(Resource):
    def get(self, applicant_id):
        if applicant_id is None:
            return None

        # Get applicant by id to get email (needed to get cv)
        with ApplicantMapper() as mapper:
            retrieved_applicant = mapper.get_by_id(applicant_id)

        # Get email from applicant
        retrieved_applicant_email = retrieved_applicant.get_email()

        # Get cv of applicant by email
        with CVMapper() as mapper:
            cv = mapper.get_by_email(retrieved_applicant_email)

            formatted_cv = {
                "id": cv.get_id(),
                "content": cv.get_content(),
            }

        # print(formatted_cv)

        return jsonify(formatted_cv)


# Class containing endpoints for /upload
class ApplicantUploadResource(Resource):

    def post(self):
        if 'cv' not in request.files or 'vacancy' not in request.form:
            return 'Required data not found in POST request.', 400

        cv_pdf_file = request.files['cv']
        vacancy_id = request.form['vacancy']

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
            face_image=applicant_face_image,
        )

        with ApplicantMapper() as applicant_mapper:
            if applicant_mapper.get_by_email(applicant.get_email()):
                # TODO: Add a new entry into the applicant_vacancy table instead of returning a 409

                return 'Applicant exists already', 409
            else:
                applicant_mapper.insert(applicant, vacancy_id)

        with CVMapper() as cv_mapper:
            cv_mapper.insert(cv_pdf_file, applicant, vacancy_id)

        model_response = rating_service.rate_applicant(applicant, vacancy_id)

        ratings = rating_service.create_rating_objects(
            model_response,
            UUID(vacancy_id),
            applicant.get_id()
        )

        for rating in ratings:
            with RatingMapper() as rating_mapper:
                rating_mapper.insert(rating)

        return 'Applicant, CV, and rating have been saved in the database', 200


# Add the resources to the API with different endpoints
api.add_resource(ApplicantListResource, '/applicants')
api.add_resource(ApplicantResource, '/applicants/<string:applicant_id>')
api.add_resource(ApplicantsByVacancyResource,
                 '/applicantsVacancy/<string:vacancy_id>')
api_upload.add_resource(ApplicantUploadResource, '/upload')
api.add_resource(ApplicantCVResource, '/applicant/<string:applicant_id>/cv')
