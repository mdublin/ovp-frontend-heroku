#A few notes on the setup here:
#this __init__.py file is in the app directory, so app directory becomes a package

#because we have no global app object (the typical app object that is created in the global scope in simple Flask project, like app = Flask(__name__) ) we cannot use the typical @app.route('/) decorators on our views functions.  
#Instead we are using Blueprints. Blueprints are containers (objects) for routes, templates, or static files. 
#Those containers are inactive. The become active when they are "registered" with the application. If you do not register it, it does nothing. But once it is hooked up to the applicaiton, all the contents of the blueprint are automatically registered with the app in one go. 


import os
from flask import Flask
from flask.ext.bootstrap import Bootstrap

from flask.ext.sqlalchemy import SQLAlchemy


#Base = declarative_base()
db = SQLAlchemy()


#flask login manager
from flask.ext.login import LoginManager

#becuase we do not have an app object that is a global object (instead app objects are created below in the app factory function create_app()) that we can pass to our instantiations of Flask extensions, we can create them here, unitialized becaue we are not passing anything to them. Then when you have app object you want, you complete the initialization of these extensions by calling .init_app(app)

bootstrap = Bootstrap()

#create SQLAlchemy database instance
# http://flask-sqlalchemy.pocoo.org/2.1/api/
#db = SQLAlchemy()


lm = LoginManager()
lm.login_view = 'main.login'

#this is function is basically logic that allows us to create an app object with whatever config we need.
#app factory that allows different configs to be utilized for app instantiation
def create_app(config_name):
    """Create an application instance."""
    app = Flask(__name__)

    # import configuration
    cfg = os.path.join(os.getcwd(), 'config', config_name + '.py')
    #import the values from a py file, which is our development.py for now. But in other modes, it could be configx.py file for whatever config you want
    app.config.from_pyfile(cfg)

    # initialize extensions
    bootstrap.init_app(app)
    db.init_app(app)
    lm.init_app(app)

    # import blueprints
    # importing from subpackage as main_blueprint has all the routes of our app (login,logout, protected, index, etc)
    # main is a directory below (actually a package, becase it has an __init__.py file which contains the actual initialization of the main Blueprint object) where this current file lives, in app parent directory. So we are .main which is importing from the directory below the current file and 
    from .main import main as main_blueprint
    # registering the blueprint with the app instance
    app.register_blueprint(main_blueprint)

    # configure production logging of errors
    #if not app.config['DEBUG'] and not app.config['TESTING']:
    #    import logging
    #    from logging.handlers import SMTPHandler
    #    mail_handler = SMTPHandler('127.0.0.1', 'error@example.com',
    #                               app.config['ADMINS'], 'Application Error')
    #    mail_handler.setLevel(logging.ERROR)
    #    app.logger.addHandler(mail_handler)
    

    return app
