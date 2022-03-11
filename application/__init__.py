"""
Created June 16, 2021
@author: oconn
"""
import os
import logging
from logging.handlers import RotatingFileHandler
from os import mkdir
from flask import Flask, current_app, request
#from application.main import routes  # From module flask import class Flask
from config import Config  # get our Configuration variables
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail, Message

#create an instance of each extention we are going to use. At this point they are not tied to a Flask app
db = SQLAlchemy()
migrate = Migrate() # Used easily changes the db structure
login = LoginManager()
login.login_view = 'auth.login'  # so Flask-Login knows which view function runs login to redirect on protected pages
mail = Mail()

def create_app(config_class=Config):
    """Now the app is created at runtime rater than the app beign a preset global variable. This fuction creates an instance of
    Flask called app. It then initailizes all of the Flask extentions and ties them to that app. When creating the app it gets some
    initail config settings from the config.py file"""
    app = Flask(__name__) # our Flask instance
    app.config.from_object(config_class) #grab those intial settings

    #now initialize all those extentions that we created 
    db.init_app(app)
    migrate.init_app(app,db)
    login.init_app(app)

    from application.errors import bp as errors_bp
    app.register_blueprint(errors_bp) #Register the Errors Blueprint with the app

    from application.auth import  bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth') #automatically add /auth to the start of all URL view funcitons registered with this BP

    from application.main import bp as main_bp
    app.register_blueprint(main_bp) #Register the Blueprint that will handle most of the routes

    if not app.debug and not app.testing: # Only run the logging when we are not running unittests or we are in Debug mode
        if not os.path.exists('logs'):
            os.mkdir('logs') # if this is your first time running the app or you deleted the log file. Make it now
        file_handler = RotatingFileHandler('logs/LockerRoom.log',
                                           maxBytes=10240, backupCount=10)
                                           # Only keep the 10 most recent sessions and limit storage size to 10KB
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.DEBUG)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.DEBUG)
        app.logger.info('LockerRoom startup')


    return app #Return the Flask instance with all the extentions initialized

# Construct an instance of Flask class for our webapp
#app = Flask(__name__)
#app.config.from_object(Config)  # dictionary style access for key
#db = SQLAlchemy(app)

#migrate = Migrate(app, db) # Now I can easily changes the db structure
#login = LoginManager(app)
#login.login_view = 'auth.login'  # so Flask-Login knows which view function runs login to redirect on protected pages
#mail = Mail(app)

#from application.errors import bp as errors_bp
#app.register_blueprint(errors_bp) #Register the Errors Blueprint with the app

#from application.auth import  bp as auth_bp
#app.register_blueprint(auth_bp, url_prefix='/auth') #automatically add /auth to the start of all URL view funcitons registered with this BP

#from application.main import bp as main_bp
#app.register_blueprint(main_bp) #Register the Blueprint that will handle most of the routes

from application import models #removed errors.py file and made it handlers.py
# work around for circular imports