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

from .methods import GroupMethod
from application.modules.user import UserMethod
from application.modules import init_logger

group_bp = Blueprint('group_bp', __name__)


# --------------------------------------- group
@group_bp.route('/group/')
@login_required
def groups():
    # Groups login
    print('----------------- group_bp.route(/group/)')
    print('current_user /group/: ', current_user)
    logger = init_logger(__name__, testing_mode=False)
    profile = current_user.profile
    print('profile: ', profile)
    # Show all group & CRUD options
    if profile == 'admin':
        # Get all groups
        all_groups = GroupMethod.get_all_groups()
    else:
        # Get all groups in which current_user is manager
        all_groups = GroupMethod.user_get_all_groups_manager(current_user.username)
    print('all_groups: ', all_groups)
    if len(all_groups) > 0:
        logger.info('Current User: {}\n'
                    '\t\tGROUP - <create - POST>: all_groups loaded successfully - len(all_groups): {}'
                    .format(current_user.username, len(all_groups)))
    else:
        logger.info('Current User: {}\n'
                    '\t\tGROUP - <create - POST>: all_groups could not be loaded - len(all_groups): 0'
                    .format(current_user.username))
    return render_template('group/group_zmenu.html',
                           groups=all_groups,
                           profile=profile)


@group_bp.route('/group/create', methods=['GET', 'POST'])
@login_required
def create():
    # Group create
    print('------------------- group_bp.create - {}'.format(request.method))
    profile = session['profile']
    logger = init_logger(__name__, testing_mode=False)
    if request.method == 'GET':
        all_users = UserMethod.get_all_users_username()
        if len(all_users) > 0:
            logger.info('Current User: {}\n'
                        '\t\tGROUP - <create - GET>: all_users loaded successfully - len(all_users): {}'
                        .format(current_user.username, len(all_users)))
        else:
            logger.warning('Current User: {}\n'
                           '\t\tGROUP - <create - GET>: all_users could not be loaded - len(all_users): 0'
                           .format(current_user.username))
        return render_template('group/group_create.html',
                               profile=profile,
                               users=all_users)
    elif request.method == 'POST':
        managers_list = GroupMethod.extract_users(request.form.getlist('managers_list'))
        users_list = GroupMethod.extract_users(request.form.getlist('users_list'))

        group_data = {
            '_id': 1,
            'name': request.form.get('name'),
            'description': request.form.get('description'),
            'user_groups_manager': managers_list,
            'user_groups': users_list
        }
        print('group_data: ', group_data)
        group_created = GroupMethod.create_group(group_data)
        if group_created:
            flash('Group created successfully')
            logger.info('Current User: {}\n'
                        '\t\tGROUP - <create - POST>: group created successfully - group_name: {}'
                        .format(current_user.username, group_data['name']))
        else:
            flash('Group could not be created')
            logger.warning('Current User: {}\n'
                           '\t\tGROUP - <create - POST>: group could not be created - group_name: {}'
                           .format(current_user.username, group_data['name']))
        return redirect(url_for('group_bp.groups',
                                profile=profile))


@group_bp.route('/group/delete/<group_name>')
@login_required
def delete(group_name: str):
    # Group delete
    print('------------------ group_bp.delete - {}'.format(group_name))
    logger = init_logger(__name__, testing_mode=False)
    profile = session['profile']
    if GroupMethod.delete_group_by_group_name(group_name):
        flash('The group <{}> has been deleted successfully'.format(group_name))
        logger.info('Current User: {}\n'
                    '\t\tGROUP - <delete>: group deleted successfully - group_name: {}'
                    .format(current_user.username, group_name))
    else:
        flash('The group <{}> could not be deleted'.format(group_name))
        logger.warning('Current User: {}\n'
                       '\t\tGROUP - <delete>: group could not be deleted - group_name: {}'
                       .format(current_user.username, group_name))
    return redirect(url_for('group_bp.groups',
                            profile=profile))


@group_bp.route('/group/read/<group_name>')
@login_required
def read(group_name: str):
    # Group read
    print('------------------ group_bp.read - {}'.format(group_name))
    logger = init_logger(__name__, testing_mode=False)
    profile = session['profile']
    group_data = GroupMethod.get_group_by_group_name(group_name)
    if group_data:
        logger.info('Current User: {}\n'
                    '\t\tGROUP - <read>: group loaded successfully - group_name: {}'
                    .format(current_user.username, group_data['name']))
    else:
        logger.warning('Current User: {}\n'
                       '\t\tGROUP - <update - POST>: group loaded successfully'
                       .format(current_user.username))
    print('group_data: ', group_data)
    return render_template('group/group_read.html',
                           group=group_data,
                           profile=profile)


@group_bp.route('/group/update/<group_name>', methods=['GET', 'POST'])
@login_required
def update(group_name: str):
    # Group update
    print('------------------ group_bp.update - {}'.format(group_name))
    logger = init_logger(__name__, testing_mode=False)
    profile = session['profile']
    if request.method == 'GET':
        group_data = GroupMethod.get_group_by_group_name(group_name)
        if group_data:
            print('GROUP - <update - GET>: group_data loaded successfully - group_name: {}'
                  .format(group_data['name']))
            logger.info('Current User: {}\n'
                        '\t\tGROUP - <update - GET>: group_data loaded successfully - group_name: {}'
                        .format(current_user.username, group_data['name']))
        else:
            print('GROUP - <update - GET>: group_data could not be loaded')
            logger.warning('Current User: {}\n'
                           '\t\tGROUP - <update - GET>: group_data could not be loaded'
                           .format(current_user.username))
        print('group_data: ', group_data)
        all_users_list = GroupMethod.only_username_list(GroupMethod.users_get_all_users_username())
        all_group_managers = group_data['managers']
        all_group_users = group_data['users']
        print('all_users_list: ', all_users_list)
        print('all_group_managers: ', all_group_managers)
        print('all_group_users: ', all_group_users)
        users = GroupMethod.extract_managers_and_users(all_users_list,
                                                       all_group_managers,
                                                       all_group_users)
        print('users: ', users)
        if len(users) > 0:
            logger.info('Current User: {}\n'
                        '\t\tGROUP - <update - GET>: users loaded successfully - len(users): {}'
                        .format(current_user.username, len(users)))
        else:
            logger.warning('Current User: {}\n'
                           '\t\tGROUP - <update - GET>: users could not be loaded - len(users): 0'
                           .format(current_user.username))
        return render_template('group/group_update.html',
                               group=group_data,
                               profile=profile,
                               users=users)
    elif request.method == 'POST':
        print('managers_list: ', request.form.getlist('managers_list'))
        print('users_list: ', request.form.getlist('users_list'))
        managers_list = GroupMethod.extract_users(request.form.getlist('managers_list'))
        users_list = GroupMethod.extract_users(request.form.getlist('users_list'))

        print('managers_list: ', managers_list)
        print('users_list: ', users_list)

        group_data = {
            'name': request.form.get('name'),
            'description': request.form.get('description'),
            'manager': managers_list,
            'user': users_list
        }
        print('group_data: ', group_data)
        if GroupMethod.update_group_data(group_name, group_data):
            logger.info('Current User: {}\n'
                        '\t\tGROUP - <update - POST>: group has been updated successfully - group_name): {}'
                        .format(current_user.username, group_data['name']))
        else:
            logger.info('Current User: {}\n'
                        '\t\tGROUP - <update - POST>: group loaded successfully - group_name: {}'
                        .format(current_user.username, group_data['name']))
    return redirect(url_for('group_bp.groups',
                            profile=profile))
