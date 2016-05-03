from flask import Blueprint

# initializing a Blueprint object called main
# the arguments to the Blueprint class are the name of the blueprint object and the Python variable __name__, which is used so that Flask knows where our application is located, it grabs the location of the package from this python variable. 
main = Blueprint('main', __name__)


from . import routes
