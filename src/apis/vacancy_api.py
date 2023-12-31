from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
import services.vacancy_service as vacancy_service
from db.mapper.mysql_mapper.vacancy_mapper import VacancyMapper as MySQLVacancyMapper
from db.mapper.mongodb_mapper.vacancy_mapper import VacancyMapper as MongoDBVacancyMapper
from classes.category import Category
import json

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
                "fullTime": vacancy.get_full_time(),
                "description": vacancy.get_description(),
                "salary": vacancy.get_salary(),
                "company": vacancy.get_company(),
                "createdAt": vacancy.get_created_at(),
                "updatedAt": vacancy.get_updated_at(),
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
                "company": vacancy.get_company(),
                "department": vacancy.get_department(),
                "salary": vacancy.get_salary(),
                "fullTime": vacancy.get_full_time(),
                "createdAt": vacancy.get_created_at(),
                "updatedAt": vacancy.get_updated_at(),
            }

            # Get categories of this vacancy
            with MongoDBVacancyMapper() as mapper:
                vacancy = mapper.get_by_id(vacancy_id)
                formatted_vacancy["categories"] = [
                    {
                        "id": category.get_id(),
                        "name": category.get_name(),
                        "guideline0": category.get_guideline_for_zero(),
                        "guideline10": category.get_guideline_for_ten(),
                    }
                    for category in vacancy.get_categories()
                ]

        return jsonify(formatted_vacancy)

class GenerateVacancyResource(Resource):
    def post(self):
        data = request.get_json()

        # Extract required data from the request payload
        basic_information = data.get('basicInformation', {})
        selected_categories = data.get('selectedCategories', [])
        adjust_prompt = data.get('adjustPrompt', '')

        generated_vacancy = vacancy_service.generate_text(basic_information, selected_categories, adjust_prompt)
        vacancy_data = json.loads(generated_vacancy)
        vacancy_text = vacancy_data.get('vacancy_text', '')

        return jsonify({'generatedVacancy': vacancy_text})

class AddVacancyResource(Resource):
    def post(self):
        data = request.get_json()

        # Extract required data from the request payload
        basic_information = data.get('basicInformation', {})
        selected_categories = data.get('selectedCategories', [])
        generated_vacancy = data.get('generatedVacancy', '')
        
        # TODO Add the vacancy using the service or mapper

        return jsonify({'message': 'Vacancy added successfully'})


# Register resources directly to the API instance
api.add_resource(VacancyListResource, '/vacancies')
api.add_resource(VacancyResource, '/vacancies/<string:vacancy_id>')
api.add_resource(GenerateVacancyResource, '/vacancies/generateVacancy')
api.add_resource(AddVacancyResource, '/vacancies/addVacancy')