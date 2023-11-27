from flask import Flask
from flask_cors import CORS

# Imports of the resources
from apis.demo_resource import demo_resource
from apis.applicant_api import file_upload

# Creates a new flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Registers the resources, which are needed.
# The (Flask-Restful)-Resources in this case are blueprints, which contain the different rest apis
app.register_blueprint(demo_resource)
app.register_blueprint(file_upload)

# Starts the flask app
if __name__ == '__main__':
    app.run()
