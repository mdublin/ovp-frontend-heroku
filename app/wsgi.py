from whitenoise import WhiteNoise
import os

# only for local testing via $ heroku local web
#config_name = os.environ.get('FLASK_CONFIG') or 'production'

config_name = os.environ.get('FLASK_CONFIG') or 'production_heroku'
#config_name = os.environ.get('production_heroku')

print(config_name)


from app import create_app, db
from app.models import User

# creating app instance
application = create_app(config_name)

#test print out to confirm config settings
print"CONFIG SETTINGS FOR VIDEO UPLOAD: "
print(application.config["ALLOWED_EXTENSIONS"])
print(application.config["UPLOAD_FOLDER"])
print(application.config["MAX_CONTENT_LENGTH"])


#application = app()
application = WhiteNoise(application, root='/app/static/')

print(application)

application.add_files('/path/to/more/static/files', prefix='more-files/')


