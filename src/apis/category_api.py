from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from db.mapper.mysql_mapper.category_mapper import CategoryMapper
from classes.category import Category
import services.category_service as category_service

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
                "guideline_for_ten": category.get_guideline_for_ten(),
                "chip": category.get_chip()
            }

        return jsonify(formatted_category)


class AllCategoriesResource(Resource):
    # Get all categories
    def get(self):
        with CategoryMapper() as mapper:
            categories = mapper.get_all()

            formatted_categories = [
                {
                    "id": str(category.get_id()),
                    "name": category.get_name(),
                    "guideline_for_zero": category.get_guideline_for_zero(),
                    "guideline_for_ten": category.get_guideline_for_ten(),
                    "chip": category.get_chip()
                }
                for category in categories
            ]

        return jsonify(formatted_categories)


class CategoryGuidelinesResource(Resource):
    # Get category guidelines by category name
    def get(self, category_name):
        if not category_name:
            return jsonify({"error": "Category name not provided"}), 400

        with CategoryMapper() as mapper:
            category = mapper.get_by_name(category_name)
            if category is not None:
                # Category already exists
                return jsonify({"error": "Category already existing"}), 404
            else:
                guidelines = category_service.get_guidelines(category_name)
                response_data = {'data': guidelines, 'status': 200}
                return response_data

class ChipForCategoryResource(Resource):
    def get(self, category_name):
        if not category_name:
            return jsonify({"error": "Category name not provided"}), 400

        with CategoryMapper() as mapper:
            category = mapper.get_by_name(category_name)
            if category is not None:
                # Category already exists
                return jsonify({"error": "Category already existing"}), 404
            else:
                # Category does not exist, call the function from category_service.py
                result = category_service.assign_chip(category_name)
                response_data = {'data': result, 'status': 200}
                return response_data


class AddCategoryResource(Resource):
    # Add a new category
    def post(self):
        category_data = request.get_json()
        if not category_data or not all(key in category_data for key in ["Name", "Chip", "Guideline_0", "Guideline_1"]):
            return jsonify({"error": "Invalid category data"}), 400

        new_category = Category(
            name=category_data["Name"],
            chip=category_data["Chip"],
            guideline_for_zero=category_data["Guideline_0"],
            guideline_for_ten=category_data["Guideline_1"]
        )

        with CategoryMapper() as mapper:
            mapper.insert(new_category)

        return jsonify({"success": "Category added successfully"})


# Add the resources to the API with different endpoints
api.add_resource(CategoryResource, '/category/<string:category_id>')
api.add_resource(AllCategoriesResource, '/allCategories')
api.add_resource(CategoryGuidelinesResource, '/getCategoryGuidelines/<string:category_name>')
api.add_resource(ChipForCategoryResource, '/getChipForCategory/<string:category_name>')
api.add_resource(AddCategoryResource, '/addCategory')
