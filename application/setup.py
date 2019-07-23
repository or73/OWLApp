"""
File Path: application/setup.py
Description: setup the App
This will have the function to create the App which will initialize the database and register all blueprints.
Copyright (c) 2019. This Application has been developed by OR73.
"""
import logging
from flask import flash, Flask, g, redirect, Markup, render_template, request, session, url_for

from werkzeug.exceptions import HTTPException
from flask_login import LoginManager
from flask_babel import Babel
from flask_pymongo import PyMongo
# We are using 'flask_pymongo' to make the DB connection object available in flask app context.
# Internally 'flask_pymongo' module uses mongoDB's python client api 'PyMongo'

# from .instance import Config
from .db_conf import JSONEncoder, URI
from application.modules import (AuxFuncs, init_logger)

babel = Babel()
login_manager = LoginManager()
mongo = PyMongo()


def create_app():
    print('------------ create_app')
    """ Initialize the core application """
    # Flask: --- Setup ----------------------------------
    app = Flask(__name__, instance_relative_config=True)
    # Flask: --- Config Setup ---------------------------
    app.config.from_object('application.instance.config.Config')
    app.config['DEBUG'] = True
    app.config['MONGO_URI'] = URI
    """ Load Configuration """

    # Flask-Babel: --- Setup ----------------------------
    babel.init_app(app)
    # Flask-login: --- Setup ----------------------------
    login_manager.init_app(app)
    # Flask-pymongo: --- Setup --------------------------
    mongo.init_app(app)
    """ Initialize plugins """
    print('<< Connected successfully with DB >>\n\t\t', mongo.db)

    login_manager.login_message = 'You must be logged in to access this page'
    login_manager.login_message_category = 'info'
    login_manager.session_protection = 'strong'
    login_manager.login_view = 'login_bp.login'

    # Logs management & configuration
    # file_handler = FileHandler.file_handler()
    logger = init_logger(__name__, testing_mode=False)
    print('-*-*-*-*-*-*-*-*-*-*-*-*-*- logger: ', logger)
    # logger.addHandler(file_handler)
    # logger.setLevel(logging.DEBUG)
    logger.info('SETUP - <create-app>: Plugins initialized successfully')

    # Use the modified encoder class to handle ObjectId & datetime object while jsonify the response
    app.json_encoder = JSONEncoder

    from application.modules import UserMethod, User
    @login_manager.user_loader
    def load_user(user_id) -> User:  # (session_token):
        print('Validating user - user_id: ', user_id)
        logger.info('SETUP - <create-app / load_user> Validating user: {}'.format(user_id))
        # user_id = UserMethod.get_id_by_session_token(session_token)
        user_to_return = UserMethod.load_user(user_id)
        if user_to_return:
            logger.info('SETUP - <create-app / load_user> User loaded successfully:\n{}'.format(user_to_return))
            if user_to_return.language != 'es':
                logger.info('SETUP - <create-app / load_users> language validated - EN')
                app.config['BABEL_DEFAULT_LOCALE'] = 'en'
            else:
                logger.info('SETUP - <create-app / load_users> language validated - ES')
        return user_to_return

    @login_manager.unauthorized_handler
    def unauthorized():
        flash('You must be logged in to view that page')
        logger.info('SETUP - <unauthorized>: Current user has not been authorized')
        return redirect(url_for('login_bp.login'))

    @babel.localeselector
    def get_locale():
        # If a user is logged in, use the Locale from the user settings
        try:
            language = session['language']
            logger.info('SETUP - <get_locale> - session language has been loaded - {}'.format(session['language']))
        except KeyError:
            # Otherwise try to guess the language from the user accept header
            #    the browser transmits.  We support 'en'/'es'
            language = request.accept_languages.best_match(app.config['LANGUAGES'].keys())
            logger.warning('SETUP - <get_locale / KeyError>: language in None, then try to guess the language\n'
                           '\tfrom the user accept header the browser transmits.  We support \'en\'/\'es\'\n'
                           '\t\tlanguage = {}'.format(language))
        return language

    @babel.timezoneselector
    def get_timezone():
        user = getattr(g, 'user', None)
        if user is not None:
            logger.info('SETUP - <get_timezone>: {}'.format(user.timezone))
            return user.timezone

    @app.context_processor
    def inject_conf_var():
        logger.info('SETUP - <inject_conf_var>: languages loading and validation')
        return dict(AVAILABLE_LANGUAGES=app.config['LANGUAGES'],
                    CURRENT_LANGUAGE=session.get('language',
                                                 request.accept_languages.best_match(app.config['LANGUAGES'].keys())))

    # --------------------------------------- Error Handler
    @app.errorhandler(Exception)
    def error_handler(error):
        print('-------------------- ERROR: - {}'.format(error.code))
        print('error: ', error)
        msg = '''Request resulted in ERROR
              CODE: {}
              MESSAGE:{}'''.format(error.code or 500, error.description or 'Internal Server Error')
        print('type(error): ', type(error))
        print('msg: ', msg)
        logger.error('SETUP - <error_handler>: An ERROR has occurred - {}\n{}'.format(msg, error))
        # exc_info=error)

        if isinstance(error, HTTPException):
            description = error.get_description(request.environ)
            code = error.code
            name = error.name
        else:
            description = ('We encountered an error'
                           'While trying to fulfill your request')
            code = 500
            name = 'Internal Server Error'
        templates_to_try = 'errors/{}.html'.format(code, 'errors/generic.html')
        prev_page = AuxFuncs.previous_page(request.path)
        print('templates_to_try: ', templates_to_try)
        return render_template(templates_to_try,
                               code=code,
                               name=Markup(name),
                               description=description,
                               error=error,
                               prev_page=prev_page)

    with app.app_context():
        """ Blueprints """
        # Blueprint for module routes in app
        from application.modules import (case_bp, group_bp, login_bp, user_bp)

        # Register Blueprints
        app.register_blueprint(case_bp)
        app.register_blueprint(group_bp)
        app.register_blueprint(login_bp)
        app.register_blueprint(user_bp)

        logger.info('SETUP - <app.app_context>: All blueprints have been loaded successfully')
        return app
