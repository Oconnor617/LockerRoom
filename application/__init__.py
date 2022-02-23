"""
Created June 16, 2021
@author: oconn
"""
from flask import Flask
#from application.main import routes  # From module flask import class Flask
from config import Config  # get our Configuration variables
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail, Message



# Construct an instance of Flask class for our webapp
app = Flask(__name__)
app.config.from_object(Config)  # dictionary style access for key
db = SQLAlchemy(app)

migrate = Migrate(app, db) # Now I can easily changes the db structure
login = LoginManager(app)
login.login_view = 'login'  # so Flask-Login knows which view function runs login to redirect on protected pages
mail = Mail(app)

from application.errors import bp as errors_bp
app.register_blueprint(errors_bp) #Register the Errors Blueprint with the app

from application.auth import  bp as auth_bp
app.register_blueprint(auth_bp, url_prefix='/auth') #automatically add /auth to the start of all URL view funcitons registered with this BP

from application.main import bp as main_bp
app.register_blueprint(main_bp) #Register the Blueprint that will handle most of the routes

from application import models #removed errors.py file and made it handlers.py
# work around for circular imports