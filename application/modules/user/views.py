"""
File path: application/modules/user/views.py
Description: Auth models for App - Define login data model
Copyright (c) 2019. This Application has been developed by OR73.
"""
# DELETE: Delete selected user
# GET: Show current user data
# POST: Create new user
# PUT: Update user data
from flask import Blueprint, flash, redirect, request, render_template, session, url_for
from flask_login import current_user, login_required

from .methods import UserMethod
from application.modules import init_logger

user_bp = Blueprint('user_bp', __name__)


# --------------------------------------- users
@user_bp.route('/user/')
@login_required
def users():
    # User login
    print('----------------- user_bp.route(/user/)')
    logger = init_logger(__name__, testing_mode=False)
    # Select user type: admin, manager or user
    print('|--- current_user: ', current_user)
    print('|--- request: ', request)
    print('|--- session: ', session)

    print('~~~~~~~~~~~~ session: ', session)
    profile = session['profile']
    user_method = []
    try:
        state = session['session_id']  # The same state value
        if profile == 'admin':
            print('---------- admin')
            user_method = UserMethod.get_all_users_name()
        elif profile == 'manager':
            print('---------- manager')
            user_method = UserMethod.get_all_users_name_manager(current_user.username)
        elif profile == 'user':
            print('---------- user')
            return redirect(url_for('case_bp.cases_user',
                                    username=current_user.username))
        else:
            # Required profile does not exist
            print('Required profile does not exist')
            logger.critical('Current User: {}\n'
                            '\t\tUSER - <users>: Required profile does not exist'
                            .format(current_user.username))
        if len(user_method) > 0:
            logger.info('Current User: {}\n'
                        '\t\tUSER - <users>: users loaded successfully - len(user_method): {}'
                        .format(current_user.username, len(user_method)))
        return render_template('user/user_zmenu.html',
                               profile=profile,
                               state=state,
                               users=user_method)
    except Exception as e:
        print('Exception in /user')
        print('error: ', e)
        logger.error('Current User: {}\n'
                     '\t\tUSER - <users>: Something wrong in users...\n'
                     '\t\tERROR: {}'
                     .format(current_user.username, e))
        return render_template('errors/404.html'), 404


@user_bp.route('/user/create/', methods=['GET', 'POST'])
@login_required
def create():
    # User create
    print('----------------- user_bp.route(/user/create/) - {}'.format(request.method))
    logger = init_logger(__name__, testing_mode=False)
    profile = session['profile']
    try:
        if request.method == 'GET':
            logger.info('Current User: {}\n'
                        '\t\tUSER - <create>: user create form loaded successfully'
                        .format(current_user.username))
            return render_template('user/user_create.html',
                                   profile=profile)
        elif request.method == 'POST':
            email_user_data = UserMethod.get_user_by_email(request.form.get('email'))
            username_user_data = UserMethod.get_user_by_username(request.form.get('username'))

            if not email_user_data:
                logger.info('Current User: {}\n'
                            '\t\tUSER - <create>: user email <{}> does not exist in DB'
                            .format(current_user.username, request.form.get('email')))
                if not username_user_data:
                    logger.info('Current User: {}\n'
                                '\t\tUSER - <create>: user username <{}> does not exist in DB'
                                .format(current_user.username, request.form.get('username')))
                    picture = None
                    if 'picture' in request.files:
                        print('picture in request files...')
                        picture = request.files['picture']
                    else:
                        print('picture is not in request files XXX')

                    email = request.form.get('email')
                    username = request.form.get('username')
                    user_data = {
                        '_id': 1,
                        'name': request.form.get('name'),
                        'username': username.replace(' ', ''),
                        'email': email.replace(' ', ''),
                        'picture': '' if not picture else picture.filename,
                        'language': request.form.get('language'),
                        'password': request.form.get('password'),
                        'profile': request.form.get('profile')
                    }
                    user_created = UserMethod.create_user(user_data, picture)
                    if user_created:
                        flash('User created successfully')
                        logger.info('Current User: {}\n'
                                    '\t\tUSER - <create>: user <{}> created successfully'
                                    .format(current_user.username, user_created['username']))
                        return redirect(url_for('user_bp.users',
                                                profile=profile))
                    else:
                        flash('User could not be created...')
                        logger.warning('Current User: {}\n'
                                       '\t\tUSER - <create>: user <{}> could not be created'
                                       .format(current_user.username, user_created['username']))
                        return redirect(url_for('user_bp.users',
                                                profile=profile))
                else:
                    flash('User username already exist in Database, try a different username')
                    logger.warning('Current User: {}\n'
                                   '\t\tUSER - <create>: user <{}> already exist in Database'
                                   .format(current_user.username, request.form.get('username')))
                    return redirect(url_for('user_bp.create',
                                            profile=profile))
            else:
                flash('User email already exist in Database, try a different email')
                logger.warning('Current User: {}\n'
                               '\t\tUSER - <create>: user email <{}> already exist in Database'
                               .format(current_user.username, request.form.get('email')))
                return redirect(url_for('user_bp.create',
                                        profile=profile))
        return redirect(url_for('user_bp.users',
                                profile=profile))
    except Exception as e:
        print('Exception in /user/create/')
        print('error: ', e)
        logger.error('Current User: {}\n'
                     '\t\tUSER - <create>: something is wrong\n\t\tException: {}'
                     .format(current_user.username, e))
        return render_template('errors/404.html'), 404


@user_bp.route('/user/delete/<username>')
@login_required
def delete(username: str):
    # User delete
    print('----------------- user_bp.route(/user/delete/)')
    print('username: ', username)
    logger = init_logger(__name__, testing_mode=False)
    try:
        profile = session['profile']
        user_delete = UserMethod.delete_user_by_username(username)
        if user_delete:
            flash('The user <{}> has been deleted successfully'.format(username))
            logger.info('Current User: {}\n'
                        '\t\tUSER - <delete>: user <{}> has been deleted successfully'
                        .format(current_user.username, username))
        else:
            flash('The user <{}> could not be deleted'.format(username))
            logger.warning('Current User: {}\n'
                           '\t\tUSER - <create>: user <{}> could not be deleted'
                           .format(current_user.username, username))
        return redirect(url_for('user_bp.users',
                                profile=profile))
    except Exception as e:
        print('Exception in /user/delete/{}'.format(username))
        print('error: ', e)
        logger.error('Current User: {}\n'
                     '\t\tUSER - <create>: something is wrong\n'
                     '\t\tException: {}'
                     .format(current_user.username, e))
        return render_template('errors/404.html'), 404


@user_bp.route('/user/image/<filename>')
@login_required
def get_user_image(filename: str):
    # Return filename image
    print('---------------- get_user_image')
    logger = init_logger(__name__, testing_mode=False)
    try:
        return UserMethod.load_user_picture(filename)
    except Exception as e:
        print('Exception in /user/image/{}'.format(filename))
        print('error: ', e)
        logger.warning('Current User: {}\n'
                       '\t\tUSER - <get_user_image>: User image could not be loaded... something is wrong!!!'
                       .format(current_user.username))
        return render_template('errors/404.html'), 404


@user_bp.route('/user/read/<username>')
@login_required
def read(username: str):
    # User read
    print('----------------- user_bp.route(/user/read/)')
    print('username: ', username)
    profile = session['profile']
    logger = init_logger(__name__, testing_mode=False)
    try:
        user_data = UserMethod.get_user_by_session_data(username)
        if user_data:
            logger.info('Current User: {}\n'
                        '\t\tUSER - <create>: user <{}> loaded successfully'
                        .format(current_user.username, username))
        else:
            logger.warning('Current User: {}\n'
                           '\t\tUSER - <create>: user <{}> could not be loaded'
                           .format(current_user.username, username))
        return render_template('user/user_read.html',
                               filename=user_data['picture'],
                               profile=profile,
                               user=user_data)

    except Exception as e:
        print('Exception in /user/read/{}'.format(username))
        print('error: ', e)
        logger.error('Current User: {}\n'
                     '\t\tUSER - <create>: something is wrong\n'
                     '\t\tException: {}'
                     .format(current_user.username, e))
        return render_template('errors/404.html'), 404


@user_bp.route('/user/settings/', methods=['GET', 'POST'])
@login_required
def settings():
    # User login
    print('----------------- user_bp.route(/user/settings)')
    logger = init_logger(__name__, testing_mode=False)
    try:
        logger.info('Current User: {}\n'
                    '\t\tUSER - <settings>: user settings loaded successfully'
                    .format(current_user.username))
        return redirect(url_for('user_bp.update',
                                username=current_user.username))
    except Exception as e:
        print('Exception in /user/settings')
        print('error: ', e)
        logger.error('Current User: {}\n'
                     '\t\tUSER - <settings>: user settings exception - exception: {}'
                     .format(current_user.username, e))
        return render_template('errors/404.html'), 404


@user_bp.route('/user/update/<username>', methods=['GET', 'POST'])
@login_required
def update(username: str):
    # User update
    print('----------------- user_bp.route(/user/update/) - {}'.format(request.method))
    print('username: ', username)
    logger = init_logger(__name__, testing_mode=False)
    profile = session['profile']
    try:
        if request.method == 'GET':
            user_data = UserMethod.get_user_by_session_data(username)
            if user_data:
                logger.info('Current User: {}\n'
                            '\t\tUSER - <update - GET>: user <{}> update format has been loaded successfully'
                            .format(current_user.username, username))
            else:
                logger.warning('Current User: {}\n'
                               '\t\tUSER - <update - GET>: user<{}> update format could not be loaded'
                               .format(current_user.username, username))
            print('current_user.username: ', current_user.username)
            print('user_data[username]: ', user_data['username'])
            print('current_user.username == user_data[username]: ', current_user.username == user_data['username'])
            return render_template('user/user_update.html',
                                   filename=user_data['picture'],
                                   is_owner=current_user.username == user_data['username'],
                                   profile=profile,
                                   user=user_data)
        elif request.method == 'POST':
            print('profile: ', profile)
            print('username: ', username)
            print('current_user.username: ', current_user.username)
            print('username == current_user.username: ', username == current_user.username)
            if (profile == 'admin' or profile == 'manager') and username != current_user.username:
                print('the user has profile of: {}\nor is owner{}'.format(profile, username == current_user.username))
                user_data = {
                    'name': request.form.get('name'),
                    'username': request.form.get('username'),
                    'email': request.form.get('email'),
                    'profile': request.form.get('profile'),
                    'active': request.form.get('active'),
                    'language': request.form.get('language')
                }
                user_update = UserMethod.update_user_data(profile, username, user_data)
                if user_update:
                    logger.info('Current User: {}\n'
                                '\t\tUSER - <update - POST>: user<{}> has been updated successfully'
                                .format(current_user.username, username))
                else:
                    logger.warning('Current User: {}\n'
                                   '\t\tUSER - <update - POST>: user<{}> could no be updated'
                                   .format(current_user.username, username))
                print('user_data: ', user_data)
                print('username: ', username)
                return redirect(url_for('user_bp.users',
                                        profile=profile))

            picture = None
            if 'picture' in request.files:
                print('picture in request files...')
                picture = request.files['picture']
            else:
                print('picture is not in request files XXX')
            user_data = {
                'name': request.form.get('name'),
                'username': request.form.get('username'),
                'email': request.form.get('email'),
                'picture': '' if not picture else picture.filename,
                'password': request.form.get('password'),
                'profile': request.form.get('profile'),
                'active': request.form.get('active'),
                'language': request.form.get('language')
            }

            user_update = UserMethod.update_user_data(profile, username, user_data, picture)
            if user_update:
                logger.info('Current User: {}\n'
                            '\t\tUSER - <update - POST>: user<{}> has been updated successfully'
                            .format(current_user.username, username))
            else:
                logger.warning('Current User: {}\n'
                               '\t\tUSER - <update - POST>: user<{}> could no be updated'
                               .format(current_user.username, username))
            print('user_data: ', user_data)
            print('username: ', username)
        return redirect(url_for('user_bp.users',
                                profile=profile))
    except Exception as e:
        print('Exception in /user/update/{}'.format(username))
        print('error: ', e)
        logger.error('Current User: {}\n'
                     '\t\tUSER - <update - POST>: user<{}> something is wrong\n'
                     '\t\tException: {}'
                     .format(current_user.username, username, e))
        return render_template('errors/404.html'), 404


@user_bp.route('/language/<language>')
def set_language(language=None):
    session['language'] = language
    logger = init_logger(__name__, testing_mode=False)
    try:
        logger.error('Current User: {}\n'
                     '\t\tUSER - <set_language>: language <{}> updated'
                     .format(current_user.username, language))
        return redirect(url_for('user_bp.users',
                                profile=session['profile']))
    except Exception as e:
        print('Exception in /language/{}'.format(language))
        print('error: ', e)
        logger.error('Current User: {}\n'
                     '\t\tUSER - <set_language>: Something is wrong - language: {}\n'
                     '\t\tException: {}'
                     .format(current_user.username, language, e))
        return render_template('errors/404.html'), 404
