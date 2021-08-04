import os
from dotenv import load_dotenv
import logging

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv()


def set_up_logging():
    """set up basic logger"""
    logging.basicConfig(level=logging.INFO)

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'my_precious'
    SQLALCHEMY_DATABASE_URI = os.environ['PRODUCTION_DB_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False