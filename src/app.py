# application dependencies
from flask import Flask

# Imports of the ressources
from resources.demo_resource import demo_resource

app = Flask(__name__)

# Registers the ressources, which are needed.
# The (Flask-RestX)-Resources in this case are blueprints, which contain the diffrent rest apis
app.register_blueprint(demo_resource)


if __name__ == '__main__':
    app.run()