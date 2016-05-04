from whitenoise import WhiteNoise
import os

# only for local testing via $ heroku local web
#config_name = os.environ.get('FLASK_CONFIG') or 'production'

config_name = os.environ.get('FLASK_CONFIG') or 'production_heroku'

from app import create_app, db
from app.models import User

# creating app instance
application = create_app(config_name)

#application = app()
application = WhiteNoise(application, root='/path/to/static/files')
application.add_files('/path/to/more/static/files', prefix='more-files/')
