from flask import Blueprint #use a Blueprint for the error handlers

bp = Blueprint('errors', __name__) # A Blueprint Instance called errors that I will use for my error handlers

from application.errors import handlers