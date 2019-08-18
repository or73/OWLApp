"""
File path: application/modules/login/views.py
Description: login views for App - Define login views
Copyright (c) 2019. This Application has been developed by OR73.
"""
from flask import Blueprint, current_app, flash, redirect, request, render_template, session, url_for
from flask_login import login_required, login_user, logout_user

from .forms import ValidateLoginForm
from .methods import LoginMethod
from application.modules import init_logger

login_bp = Blueprint('login_bp', __name__)


@login_bp.route('/', methods=['GET', 'POST'])
@login_bp.route('/login/', methods=['GET', 'POST'])
def login():
    languages = {'en': 'English', 'es': 'Español'}
    # Login local user
    print('----------------- login %s' % request.method)
    logger = init_logger(__name__, testing_mode=False)
    state = LoginMethod.generate_state_var()
    print('state: ', state)

    if request.method == 'GET':
        current_app.logger.info('LOGIN - <login - GET>: Login form loaded successfully')
        return render_template('login/login.html',
                               state=state)
    if request.method == 'POST':
        print('POST method running for login_bp - Validating User')
        logger.info('LOGIN - <login - POST>: Login form received successfully')
        # Validate login form
        validate_login_form = ValidateLoginForm(request.form)
        logger.info('LOGIN - <login - POST>: Login form send to validation')
        print('validate_login_form: ', validate_login_form)
        if validate_login_form.validate():
            print('|--> Login form validated')
            logger.info('LOGIN - <login - POST>: Login form has been validated successfully for user: <{}>'
                        .format(validate_login_form.email.data))
            # Catch user & password
            email_or_username = validate_login_form.email.data
            password = validate_login_form.password.data
            remember = validate_login_form.remember.data

            print('email_or_username: ', email_or_username)
            email = LoginMethod.get_user_email_by_email_or_username(email_or_username)
            print('email: ', email)

            if email:
                # Validate that user exists
                user_from_db_by_email = LoginMethod.get_user_by_email(email)
                user = LoginMethod.user_method_validate_user(user_from_db_by_email, password)
                print('******* ****** type(user): ', type(user))
                # Check if user actually exists take the login supplied password, hash it,
                #   and compare it to the hashed password in the database if not login or
                #   not check_password_hash(login.password, password
                if not user:
                    print('Provided user email doesn\'t exist, invalid password or user is not active')
                    flash('Something is wrong!!!\n'
                          '\t- Provided email doesn\'t exist\n'
                          '\t- Invalid password\n'
                          '-\tUser is not active')
                    logger.warning('LOGIN - <login - POST>: Something is wrong!!!:\n'
                                   '\t- Provided email doesn\'t exist'
                                   '\t- Invalid password'
                                   '\t- User is not active')
                    return redirect(url_for('login_bp.login',
                                            state=state))
                print('|--> user: ', user)
                # Add the user to session environment
                login_user(user, remember=remember)
                print('The user has been added to current session environment...')

                # Update session data
                session_data = LoginMethod.user_method_session_data(user, state)
                print('Session data updated... session_data: ', session_data)
                update_session(session_data)
                print('Session data updated... session: ', session)

                # Create login register
                new_login = LoginMethod.create_login(user_id=LoginMethod.user_method_get_user_id(user))
                print('new_login: \n', new_login)

                if not new_login:
                    flash('Something was wrong, and session could not be initiated... try again')
                    return redirect(url_for('login_bp.login'))
                flash('Successful Login')
                print('Successful Login')
                print('session: ', session)
                logger.info('LOGIN - <login>: User {} has logged in successfully '.format(email))
                print('-*-*-*-*-*-*-*-*-*-*-*-*-*- User Login')

                language_class = 'flag-icon-co' if session['language'] == 'es' else 'flag-icon-us'
                return redirect(url_for('case_bp.cases_user_login',
                                        language_class=language_class,
                                        state=state))
        else:
            flash('Some provided data is not valid or wrong')
            logger.warning('LOGIN - <login - POST>: A user has provided wrong data ')
            return redirect(url_for('login_bp.login'))


@login_bp.route('/logout/')
@login_required
def logout():
    # Logout & Close current session
    print('-------------------- logout')
    logger = init_logger(__name__, testing_mode=False)
    try:
        logout_user()
        print('session: ', session)
        print('session[access_token]: ', session['access_token'])
        logger.info('LOGIN - <logout>: User {} has logged out successfully '.format(session['email']))
        # Update logout-time in session collection
        LoginMethod.update_logout_time(session['access_token'])
        del session['access_token']
        del session['authenticated']
        del session['email']
        del session['profile']
        del session['session_id']
        del session['username']
        session.modified = True
        return redirect(url_for('login_bp.login'))
    except Exception as e:
        logger.error('LOGIN - <logout>: User {} could not logged out successfully - ERROR: {}'
                     .format(session['username'], e))


# ------------------------ General Methods
def update_session(session_data: dict) -> None:
    # Store all provided data in the current session
    print('------------------- update_session')
    logger = init_logger(__name__, testing_mode=False)
    session['access_token'] = session_data['access_token']
    session['authenticated'] = session_data['authenticated']
    session['email'] = session_data['email']
    session['profile'] = session_data['profile']
    session['provider'] = session_data['provider']
    session['session_id'] = session_data['session_id']
    session['username'] = session_data['username']
    logger.info('update_session: session has been updated successfully')
