# Classes
from classes.applicant import Applicant
# Mapper
from db.mapper.mongodb_mapper.cv_mapper import CVMapper
from db.mapper.mysql_mapper.applicant_mapper import ApplicantMapper
from db.mapper.mysql_mapper.rating_mapper import RatingMapper
from db.mapper.mysql_mapper.vacancy_mapper import VacancyMapper
#Services
import services.cv_service as cv_service
import services.pdf_service as pdf_service
import services.rating_service as rating_service
# Other packages
from flask import Blueprint, request, jsonify, send_file, Response
from flask_restful import Api, Resource
from uuid import UUID
import base64
import io

# Creates a new blueprint for upload
file_upload = Blueprint("file_upload", __name__)
api_upload = Api(file_upload)


# Creates a new blueprint for listing applicants
applicant_list = Blueprint("applicant_list", __name__)
api = Api(applicant_list)


class ApplicantListResource(Resource):
    """Class containing all the methods to handle all applicants

    Args:
        Resource (Resource): Inherits Resource class of flask_restful
    """

    def encode_image(self, image_data: bytes) -> str | None:
        """Encodes image data

        Args:
            image_data (bytes): Data of image, which should be encoded

        Returns:
            str | None: The encoded encoded image
        """
        if image_data is not None:
            return base64.b64encode(image_data).decode("utf-8")
        else:
            return None


    def get(self) -> Response:
        """Returns all the applicants from the database

        Returns:
            Response: All applicants
        """
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

class ApplicantsByVacancyResource(Resource):
    """Class containing all the methods to handle applicants by vacancy id


    Args:
        Resource (Resource): Inherits Resource class of flask_restful
    """

    def encode_image(self, image_data: bytes) -> str | None:
        """Encodes image data

        Args:
            image_data (bytes): Data of image, which should be encoded

        Returns:
            str | None: The encoded encoded image
        """
        if image_data is not None:
            return base64.b64encode(image_data).decode("utf-8")
        else:
            return None

    def get(self, vacancy_id: UUID) -> Response:
        """Returns all applicants based on a vacancy_id

        Args:
            vacancy_id (UUID): Id of the vacancy

        Returns:
            Response: All applicants 
        """
        with ApplicantMapper() as mapper:
            applicants = mapper.get_by_vacancy_id(vacancy_id)

            formatted_applicants = []
            for applicant in applicants:
                applicant_id = applicant.get_id()

                total_score = mapper.get_total_score(applicant_id, vacancy_id)

                formatted_applicants.append({
                    "id": applicant_id,
                    "firstName": applicant.get_first_name(),
                    "lastName": applicant.get_last_name(),
                    "img": self.encode_image(applicant.get_face_image()),
                    "DateOfBirth": applicant.get_date_of_birth(),
                    "street": applicant.get_street(),
                    "postalCode": applicant.get_postal_code(),
                    "city": applicant.get_city(),
                    "email": applicant.get_email(),
                    "phoneNumber": applicant.get_phone_number(),
                    "totalScore": total_score,
                })

        return jsonify(formatted_applicants)


class ApplicantResource(Resource):
    """Class containing all the methods to handle single applicants

    Args:
        Resource (Resource): Inherits Resource class of flask_restful
    """

    def encode_image(self, image_data: bytes) -> str | None:
        """Encodes image data

        Args:
            image_data (bytes): Data of image, which should be encoded

        Returns:
            str | None: The encoded encoded image
        """
        if image_data is not None:
            return base64.b64encode(image_data).decode("utf-8")
        else:
            return None

    def get(self, applicant_id: UUID, vacancy_id: UUID) -> Response:
        """Returns an applicant based on the applicant_id and a vacancy_id

        Args:
            applicant_id (UUID): Id if the applicant
            vacancy_id (UUID): Id of the vacancy

        Returns:
            Response: The applicant
        """
        if applicant_id is None:
            return None

        with ApplicantMapper() as mapper:
            applicant = mapper.get_by_id(applicant_id)
            total_score = mapper.get_total_score(applicant_id, vacancy_id)

            formatted_applicant = {
                "id": applicant.get_id(),
                "firstName": applicant.get_first_name(),
                "lastName": applicant.get_last_name(),
                "img": self.encode_image(applicant.get_face_image()),
                "DateOfBirth": applicant.get_date_of_birth(),
                "street": applicant.get_street(),
                "postalCode": applicant.get_postal_code(),
                "city": applicant.get_city(),
                "email": applicant.get_email(),
                "phoneNumber": applicant.get_phone_number(),
                "totalScore": total_score,
            }

        return jsonify(formatted_applicant)


class ApplicantCVResource(Resource):
    """Class containing all the methods to handle the cv of an applicant

    Args:
        Resource (Resource): Inherits Resource class of flask_restful
    """

    def get(self, applicant_id: UUID, vacancy_id: UUID) -> tuple:
        """Returns the CV of a applicant

        Args:
            applicant_id (UUID): Id of applicant
            vacancy_id (UUID): Id of vacancy

        Returns:
            tuple: The CV
        """
        if applicant_id is None:
            return "Applicant id is missing", 400
        if vacancy_id is None:
            return "Vacancy id is missing", 400

        # Get the cv from the database
        with CVMapper() as cv_mapper:
            retrieved_cv_name, retrieved_cv_bytes = cv_mapper.get_by_id(
                applicant_id, vacancy_id)

        # Check if the cv was found
        if retrieved_cv_bytes is None:
            return "CV not found", 404

        # return bytes as pdf file
        return send_file(
            io.BytesIO(retrieved_cv_bytes),
            download_name=retrieved_cv_name,
            mimetype="application/pdf",
        )


# Class containing endpoints for /upload
class ApplicantUploadResource(Resource):
    """Class containing all the methods to handle applicant uploads

    Args:
        Resource (Resource): Inherits Resource class of flask_restful
    """

    def post(self) -> tuple:
        """Adds a new applicant

        Returns:
            tuple: Http response
        """
        if "cv" not in request.files or "vacancy" not in request.form:
            return "Required data not found in POST request.", 400

        cv_pdf_file = request.files["cv"]
        vacancy_id = request.form["vacancy"]

        applicant_face_image = cv_service.process_cv_image(cv_pdf_file)
        cv_content_string = pdf_service.getPdfContent(cv_pdf_file)
        personal_data = cv_service.get_personal_data_from_cv(cv_content_string)

        applicant = Applicant(
            personal_data["first_name"],
            personal_data["last_name"],
            personal_data["date_of_birth"],
            personal_data["street"],
            personal_data["postal_code"],
            personal_data["city"],
            personal_data["email"],
            personal_data["phone_number"],
            applicant_face_image,
        )

        with ApplicantMapper() as applicant_mapper:
            # Check if applicant already exists in the database
            if applicant_mapper.get_by_email(applicant.get_email()):
                # Check if the applicant already applied for the vacancy
                applicant_id = applicant_mapper.get_by_email(
                    applicant.get_email()).get_id()
                applicant = applicant_mapper.get_by_email(
                    applicant.get_email())

                vacancy_applicants = applicant_mapper.get_by_vacancy_id(
                    vacancy_id)
                # Extrahiere die IDs aus der Liste der Applicant-Objekte
                vacancy_applicant_ids = [applicant.get_id()
                                         for applicant in vacancy_applicants]

                if applicant_id in vacancy_applicant_ids:
                    return "Applicant already applied for this vacancy", 400
                else:

                    # First get the applicant id
                    retrieved_applicant_id = applicant_mapper.get_by_email(
                        applicant.get_email()).get_id()
                    # Then create a new entry in the applicant_vacancy table
                    applicant_mapper.insert_into_applicant_vacancy(
                        str(retrieved_applicant_id), vacancy_id
                    )
            else:
                applicant_mapper.insert(applicant, vacancy_id)

        # Insert the cv into the document database
        with CVMapper() as cv_mapper:
            cv_mapper.insert(cv_pdf_file, applicant, vacancy_id)

        # Create a rating for the applicant
        ratings = rating_service.rate_applicant_and_create_rating_objects(
            cv_content_string, applicant, vacancy_id)

        total_score = 0
        # Insert the ratings into the database
        for rating in ratings:
            with VacancyMapper() as vacancy_mapper:
                weight = vacancy_mapper.get_weight_by_vacancy_category_ids(
                    rating.get_vacancy_id(), rating.get_category_id())
                total_score += float(weight) * float(rating.get_score()) / 100
            rating.get_score
            with RatingMapper() as rating_mapper:
                rating_mapper.insert(rating)

        with ApplicantMapper() as applicant_mapper:
            # Insert total score into the database
            applicant_mapper.update_total_score(
                applicant.get_id(), vacancy_id, total_score)

        return "Applicant, CV, and rating have been saved in the database", 200


# Add the resources to the API with different endpoints
api.add_resource(ApplicantListResource, "/applicants")
api.add_resource(ApplicantResource,
                 "/applicants/<string:applicant_id>/<string:vacancy_id>")
api.add_resource(ApplicantsByVacancyResource,
                 "/applicantsVacancy/<string:vacancy_id>")
api_upload.add_resource(ApplicantUploadResource, "/upload")
api.add_resource(ApplicantCVResource,
                 "/applicant/<string:applicant_id>/cv/<string:vacancy_id>/cv.pdf")
