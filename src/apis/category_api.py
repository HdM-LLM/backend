# Classes
from classes.category import Category
# Mapper
from db.mapper.mysql_mapper.category_mapper import CategoryMapper
# Services
import services.category_service as category_service
# Other Packages
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from uuid import UUID


category_api = Blueprint('category_api', __name__)
api = Api(category_api)


class CategoryResource(Resource):
    """Class containing all the methods to handle single categories

    Args:
        Resource (Resource): Inherits Resource class of flask_restful
    """

    def get(self, category_id: UUID) -> tuple:
        """Returns category by id

        Args:
            category_id (UUID): Id of the category

        Returns:
            tuple: The category
        """
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
    """Class containing all the methods to handle all categories

    Args:
        Resource (Resource): Inherits Resource class of flask_restful
    """

    def get(self) -> tuple:
        """Returns all categories

        Returns:
            tuple: The categories
        """
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
    """Class containing all the methods to handle single categories by category_name

    Args:
        Resource (Resource): Inherits Resource class of flask_restful
    """

    def get(self, category_name: str) -> tuple:
        """Returns category by its name

        Args:
            category_name (str): The name of the category

        Returns:
            tuple: The category
        """
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
    """Class containing all the methods to handle category chips

    Args:
        Resource (Resource): Inherits Resource class of flask_restful
    """

    def get(self, category_name: str) -> tuple:
        """Returns chip for a category

        Args:
            category_name (str): The name of the category

        Returns:
            tuple: The chip
        """
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
    """Class containing all the methods to add categories

    Args:
        Resource (Resource): Inherits Resource class of flask_restful
    """

    def post(self) -> tuple:
        """Adds category

        Returns:
            tuple: The response
        """
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
api.add_resource(CategoryGuidelinesResource,
                 '/getCategoryGuidelines/<string:category_name>')
api.add_resource(ChipForCategoryResource,
                 '/getChipForCategory/<string:category_name>')
api.add_resource(AddCategoryResource, '/addCategory')
