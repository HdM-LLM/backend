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


rating_api = Blueprint('rating_api', __name__)
api = Api(rating_api)


class RatingResource(Resource):

    # Get rating by vacancy id and applicant id
    def get(self, vacancy_id, applicant_id):
        if vacancy_id is None:
            return jsonify({"error": "Vacancy ID is required"}), 400
        if applicant_id is None:
            return jsonify({"error": "Applicant ID is required"}), 400

        with RatingMapper() as mapper:
            ratings = mapper.get_by_id(vacancy_id, applicant_id)
            if ratings is None:
                return jsonify({"error": "Rating not found"}), 404

            formatted_ratings = [
                {
                    "id": rating.get_id(),
                    "categoryId": rating.get_category_id(),
                    "vacancyId": rating.get_vacancy_id(),
                    "applicantId": rating.get_applicant_id(),
                    "score": rating.get_score(),
                    "justification": rating.get_justification(),
                    "quote": rating.get_quote(),
                }
                for rating in ratings
            ]

        return jsonify(formatted_ratings)


# Add the resources to the API with different endpoints
api.add_resource(
    RatingResource, '/applicantsRating/<string:vacancy_id>/<string:applicant_id>')
