"""
Created on June 16
@author: oconn
"""
# Separation of concerns - keep the configuration in a separate place from where we create our app
# Our Configuration is stored in our App projects top-level directory
import os #, sys
# from utils import Utils

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """We will store our configuration setting as class variables in the config class """
    SECRET_KEY = os.environ.get('SECRET_KEY)') or 'you-will-never-guess'
    # ...
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
