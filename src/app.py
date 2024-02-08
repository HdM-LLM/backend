"""
Module for initializing and running the Flask application.
"""
from flask import Flask
from flask_cors import CORS

# Imports of the resources
from apis.demo_resource import demo_resource
from apis.applicant_api import file_upload, applicant_list
from apis.vacancy_api import vacancy_api
from apis.rating_api import rating_api
from apis.category_api import category_api

# Creates a new flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Registers the resources, which are needed.
# The (Flask-Restful)-Resources in this case are blueprints, which contain the different rest apis
app.register_blueprint(demo_resource)
app.register_blueprint(file_upload)
app.register_blueprint(applicant_list)
app.register_blueprint(vacancy_api)
app.register_blueprint(rating_api)
app.register_blueprint(category_api)


# Starts the flask app
if __name__ == '__main__':
    app.run()
