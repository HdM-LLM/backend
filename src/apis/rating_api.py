# Classes
# Mapper
# Services
# Enums
# Other packages

# Mapper
from db.mapper.mysql_mapper.rating_mapper import RatingMapper
# Other packages
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from uuid import UUID


rating_api = Blueprint('rating_api', __name__)
api = Api(rating_api)


class RatingResource(Resource):
    """Class containing all the methods to handle a single rating

    Args:
        Resource (Resource): Inherits Resource class of flask_restful
    """

    def get(self, vacancy_id: UUID, applicant_id: UUID) -> tuple:
        """Returns rating based on vacancy_id and applicant_id

        Args:
            vacancy_id (UUID): Id of the vacancy
            applicant_id (UUID): Id of the applicant

        Returns:
            tuple: The rating
        """
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
                    "weight": rating.get_weight(),
                }
                for rating in ratings
            ]

        return jsonify(formatted_ratings)


# Add the resources to the API with different endpoints
api.add_resource(
    RatingResource, '/applicantsRating/<string:vacancy_id>/<string:applicant_id>')
