from flask import Blueprint
from flask_restful import Api, Resource

# Creates a new blueprint
demo_resource = Blueprint('demo_resource', __name__)
api = Api(demo_resource)


# Create a new resource
class DemoRestResource(Resource):

    # Create a get request for the resource
    def get(self):
        return 'Hello World!'


# Add the resource to the api
api.add_resource(DemoRestResource, '/demo')
