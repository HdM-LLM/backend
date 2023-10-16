# application dependencies
from flask import Flask

# Imports of the resources
from resources.demo_resource import demo_resource

app = Flask(__name__)

# Registers the resources, which are needed.
# The (Flask-Restful)-Resources in this case are blueprints, which contain the different rest apis
app.register_blueprint(demo_resource)


if __name__ == '__main__':
    app.run()