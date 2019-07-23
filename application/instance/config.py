"""
File Path: application/instance/config.py
Description: Application Constants
Copyright (c) 2019. This Application has been developed by OR73.
"""
import ast
import os
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    """ Set Flask configuration vars """
    # General Config
    FLASK_APP: str = os.environ.get('APP')
    FLASK_DEBUG: bool = os.environ.get('DEBUG', default=True)
    FLASK_ENV: str = os.environ.get('ENV')
    APP: str = os.environ.get('APP')
    DEBUG: bool = os.environ.get('DEBUG', default=True)
    ENV: str = os.environ.get('ENV')
    SECRET_KEY: str = os.environ.get('SECRET_KEY')

    # Database Settings
    MONGODB_AUTH_DB: str = os.environ.get('MONGODB_AUTH_DB')
    MONGODB_DB: str = os.environ.get('MONGODB_DB')
    MONGODB_HOST: str = os.environ.get('MONGODB_HOST')
    MONGODB_PORT: int = int(os.environ.get('MONGODB_PORT'))
    MONGODB_USERNAME: str = os.environ.get('MONGODB_USERNAME')
    MONGODB_PASSWORD: str = (os.environ.get('MONGODB_PWD'))

    # Languages - Babel
    LANGUAGES = ast.literal_eval(os.environ.get('LANGUAGES'))
