import os
import urlparse

ADMINS = ['admin@test.com']
DEBUG = False
SECRET_KEY = 'top secret!'


# if you are running this configuration locally, just export DATABASE_URL environment variable so you can connect to your local PostgreSQL database (or just insert the actual psql URL as you see in the other config files)
# But for Heroku deploy, this will suffice as the Heroku environment already sets DATABASE_URL to the psql url of the db istance, which is actually hosted on Amazon AWS. 
SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]


UPLOAD_FOLDER = "./app/ovpAPI/uploads"
#UPLOAD_FOLDER = os.environ["UPLOAD_FOLDER"]

UPLOAD_FOLDER_GET = "/app/ovpAPI/uploads"
# permitted video file extensions
ALLOWED_EXTENSIONS = set(['mov', 'mp4', 'mpeg', 'mpg', 'flv', 'avi'])
#ALLOWED_EXTENSIONS = os.environ["ALLOWED_EXTENSIONS"]
# set max file upload size, right now 900MB
MAX_CONTENT_LENGTH = 900 * 1024 * 1024
#MAX_CONTENT_LENGTH = os.environ["MAX_CONTENT_LENGTH"]


# if you're trying to serve Bootstrap locally from within app vs CDN, set this to True.
# https://pythonhosted.org/Flask-Bootstrap/configuration.html
#
#BOOTSTRAP_SERVE_LOCAP = True
