### The __init__ file for my Authentication view functions and Blueprint
from flask import Blueprint

bp = Blueprint('auth', __name__)

from application.auth import routes #import the view funcitons for authentication