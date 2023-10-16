# application dependencies
from flask import Flask
from flask_cors import CORS

# Imports of the resources
from resources.demo_resource import demo_resource

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Registers the resources, which are needed.
# The (Flask-Restful)-Resources in this case are blueprints, which contain the different rest apis
app.register_blueprint(demo_resource)


if __name__ == '__main__':
    app.run()