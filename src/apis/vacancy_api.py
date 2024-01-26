from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
import services.vacancy_service as vacancy_service
from classes.vacancy import Vacancy
from db.mapper.mysql_mapper.vacancy_mapper import VacancyMapper as MySQLVacancyMapper
from db.mapper.mongodb_mapper.vacancy_mapper import VacancyMapper as MongoDBVacancyMapper
from db.mapper.mysql_mapper.category_mapper import CategoryMapper
from classes.category import Category
import json
from enums.workingHour import WorkingHour
from enums.department import Department

vacancy_api = Blueprint('vacancy_api', __name__)
api = Api(vacancy_api)


class VacancyListResource(Resource):
    def get(self):
        with MySQLVacancyMapper() as vacancy_mapper:
            vacancies_data = vacancy_mapper.get_all()

        formatted_vacancies = [
            {
                "id": vacancy.get_id(),
                "title": vacancy.get_title(),
                "department": vacancy.get_department(),
                "working_time": vacancy.get_working_hours(),
                "description": vacancy.get_description(),
            }
            for vacancy in vacancies_data
        ]

        return jsonify(formatted_vacancies)


class VacancyResource(Resource):
    def get(self, vacancy_id):
        if vacancy_id is None:
            return jsonify({"error": "Vacancy ID is required"}), 400
        with MySQLVacancyMapper() as mapper:
            vacancy = mapper.get_by_id(vacancy_id)
            if vacancy is None:
                return jsonify({"error": "Vacancy not found"}), 404

            formatted_vacancy = {
                "id": vacancy.get_id(),
                "title": vacancy.get_title(),
                "description": vacancy.get_description(),
                "department": vacancy.get_department(),
            }
            formatted_categories = []

            # Get categories of this vacancy
            categories = mapper.get_all_categories_by_vacancy_id(vacancy_id)

            for category in categories:
                formatted_category = {
                    "id": category.get_id(),
                    "name": category.get_name(),
                    "chip": category.get_chip(),
                    "guideline_for_zero": category.get_guideline_for_zero(),
                    "guideline_for_ten": category.get_guideline_for_ten(),
                }
                formatted_categories.append(formatted_category)

        return jsonify(formatted_vacancy)

class GenerateVacancyResource(Resource):
    def post(self):
        data = request.get_json()

        # Extract required data from the request payload
        basic_information = data.get('basicInformation', {})
        selected_categories = data.get('selectedCategories', [])
        adjust_prompt = data.get('adjustPrompt', '')

        generated_vacancy = vacancy_service.generate_text(basic_information, selected_categories, adjust_prompt)
        vacancy_text = generated_vacancy.get('vacancy_text', '')

        return jsonify({'generatedVacancy': vacancy_text})

class AddVacancyResource(Resource):
    def post(self):
        data = request.get_json()

        # Extract required data from the request payload
        basic_information = data.get('basicInformation', {})
        selected_categories = data.get('selectedCategories', [])
        generated_vacancy = data.get('generatedVacancy', '')

        existing_categories = []
        category_weights = []
        
        for category in selected_categories:
            with CategoryMapper() as category_mapper:
                existing_category = category_mapper.get_by_id(category['id'])
                existing_categories.append(existing_category)
                category_weights.append(category['weight'])

        vacancy = Vacancy(
            basic_information['title'],
            Department[basic_information['department'].upper()].value,
            WorkingHour[basic_information['workingHours'].upper()].value,
            basic_information['description']
        )

        with MySQLVacancyMapper() as vacancy_mapper:
            vacancy_mapper.insert(vacancy)

            for category, weight in zip(existing_categories, category_weights):
                    vacancy_mapper.insert_vacancy_category_relation(vacancy, category, weight)

        with MongoDBVacancyMapper() as vacancy_mapper:
            vacancy_mapper.insert(generated_vacancy, vacancy)

        return jsonify({'message': 'Vacancy added successfully'})


# Register resources directly to the API instance
api.add_resource(VacancyListResource, '/vacancies')
api.add_resource(VacancyResource, '/vacancies/<string:vacancy_id>')
api.add_resource(GenerateVacancyResource, '/vacancies/generateVacancy')
api.add_resource(AddVacancyResource, '/vacancies/addVacancy')