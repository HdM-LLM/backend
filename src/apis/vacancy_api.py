from flask import Blueprint, jsonify
from flask_restful import Api, Resource

from db.mapper.mysql_mapper.vacancy_mapper import VacancyMapper

vacancy_api= Blueprint('vacancy_api', __name__)
api = Api(vacancy_api)

class VacancyListResource(Resource):
    def get(self):
        with VacancyMapper() as vacancy_mapper:
            vacancies_data = vacancy_mapper.get_all()

        formatted_vacancies = [
            {
                "id": vacancy.get_id(),
                "vacancyTitle": vacancy.get_vacancy_title(),
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
        with VacancyMapper() as vacancy_mapper:
            vacancy = vacancy_mapper.get_by_id(vacancy_id)
            if not vacancy:
                return jsonify({"error": "Vacancy not found"}), 404

        formatted_vacancy = {
            "id": vacancy.get_id(),
            "vacancyTitle": vacancy.get_vacancy_title(),
            "department": vacancy.get_department(),
            "fullTime": vacancy.get_full_time(),
            "description": vacancy.get_description(),
            "salary": vacancy.get_salary(),
            "company": vacancy.get_company(),
            "createdAt": vacancy.get_created_at(),
            "updatedAt": vacancy.get_updated_at(),
        }

        return jsonify(formatted_vacancy)

# Register resources directly to the API instance
api.add_resource(VacancyListResource, '/vacancies', endpoint='vacancies')
api.add_resource(VacancyResource, '/vacancies/<string:vacancy_id>', endpoint='vacancy_by_id')
