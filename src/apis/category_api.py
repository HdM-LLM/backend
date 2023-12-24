from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from db.mapper.mongodb_mapper.category_mapper import CategoryMapper
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


category_api = Blueprint('category_api', __name__)
api = Api(category_api)


class CategoryResource(Resource):

    # Get category by rating id
    def get(self, category_id):
        if not category_id:
            return jsonify({"error": "Category id not found"}), 404

        with CategoryMapper() as mapper:
            category = mapper.get_by_id(category_id)
            if category is None:
                return jsonify({"error": "Category not found"}), 404

            formatted_category = {
                "id": str(category.get_id()),
                "name": category.get_name(),
                "guideline_for_zero": category.get_guideline_for_zero(),
                "guideline_for_ten": category.get_guideline_for_ten()
            }

        return jsonify(formatted_category)


# Add the resources to the API with different endpoints
api.add_resource(CategoryResource, '/category/<string:category_id>')
