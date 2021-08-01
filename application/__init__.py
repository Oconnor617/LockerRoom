"""
Created June 16, 2021
@author: oconn
"""
from flask import Flask  # From module flask import class Flask
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

from application import routes, models, errors
# work around for circular imports