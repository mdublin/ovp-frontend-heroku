from whitenoise import WhiteNoise
import os

#config_name = os.environ.get('FLASK_CONFIG') or 'production_heroku'

config_name = os.environ.get('FLASK_CONFIG') or 'production'


from app import create_app, db
from app.models import User


#creating app instance
application = create_app(config_name)

#with application.app_context():
    #db.drop_all(engine)
#    db.create_all()
#    User.register('john', 'some@email.com', 'cat') 


#application = app()
application = WhiteNoise(application, root='/path/to/static/files')
application.add_files('/path/to/more/static/files', prefix='more-files/')
