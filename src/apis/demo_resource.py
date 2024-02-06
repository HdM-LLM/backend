# Other packages
from flask import Blueprint
from flask_restful import Api, Resource

# Creates a new blueprint
demo_resource = Blueprint('demo_resource', __name__)
api = Api(demo_resource)


class DemoRestResource(Resource):
    """Class containing demo method

    Args:
        Resource (Resource): Inherits Resource class of flask_restful
    """

    def get(self) -> str:
        """Returns hello world example

        Returns:
            str: Hello World!
        """
        return 'Hello World!'


# Add the resource to the api
api.add_resource(DemoRestResource, '/demo')
