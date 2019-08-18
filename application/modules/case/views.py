"""
File path: application/modules/case/views.py
Description: Auth models for App - Define login data model
Copyright (c) 2019. This Application has been developed by OR73.
"""
# DELETE: Delete selected user
# GET: Show current user data
# POST: Create new user
# PUT: Update user data
from flask import Blueprint, flash, redirect, request, render_template, session, url_for
from flask_login import current_user, login_required

from .methods import CaseMethod
from ..group import GroupMethod

from application.modules import init_logger

case_bp = Blueprint('case_bp', __name__)


# --------------------------------------- cases
@case_bp.route('/case/<case_name>')
@login_required
def case_environment (case_name: str):
    # Create case environment
    print('------------------- case_bp.route(/case/{})'.format(case_name))
    logger = init_logger(__name__, testing_mode=False)
    logger.info('Current User: {}\n'
                '\t\tCASE - <case_environment>: The case <{}> has been selected'
                .format(current_user.username, case_name))
    return None


@case_bp.route('/case/')
@login_required
def cases():
    # Cases login
    print('----------------- case_bp.route(/cases/)')
    logger = init_logger(__name__, testing_mode=False)
    # Select user type: admin, manager or user
    print('|--- current_user: ', current_user)
    print('|--- request: ', request)
    print('|--- session: ', session)
    profile = session['profile']
    state = session['session_id']  # The same state value
    all_groups = CaseMethod.get_all_groups_name()
    print('len(all_groups): ', len(all_groups))
    if len(all_groups) > 0:
        logger.info('Current User: {}\n'
                    '\t\tCASE - <cases>: all_groups have been loaded successfully - len(all_groups): {}'
                    .format(current_user.username, len(all_groups)))
    else:
        logger.warning('Current User: {}\n'
                       '\t\tCASE - <cases>: all_groups could not be loaded - 0'
                       .format(current_user.username))
    print('case - session: ', session)
    print('case - profile: ', profile)
    # Get all cases
    all_cases = CaseMethod.get_all_cases()
    if len(all_cases) > 0:
        logger.info('Current User: {}\n'
                    '\t\tCASE - <cases>: all_cases have been loaded successfully - len(all_cases): {}'
                    .format(current_user.username, len(all_cases)))
    else:
        logger.warning('Current User: {}\n'
                       '\t\tCASE - <cases>: all_cases could not be loaded - len(all_cases): 0'
                       .format(current_user.username))
    print('all_cases: ', all_cases)
    # Show all cases & CRUD options
    return render_template('case/case_zmenu.html',
                           cases=all_cases,
                           groups=all_groups,
                           profile=profile,
                           state=state)


@case_bp.route('/cases/allGroups/')
@login_required
def allGroups():
    print('----------------- case_bp.route(/cases/allGroups/)')
    allGroupsName = CaseMethod.get_all_groups_name()
    groupsList = []
    print('allGroupsName: ', allGroupsName)
    for group in allGroupsName:
        groupsList.append(group['name'])
    print('groupsList: ', groupsList)
    return {'groupsList': groupsList}


@case_bp.route('/cases/<username>')
@login_required
def cases_user (username: str):
    print('------------------ case_bp.route(/case/{})'.format(username))
    logger = init_logger(__name__, testing_mode=False)
    # if current_user_profile == 'user':
    print('Current User: {}\n'
          '\t\tCASE - <cases/{}>: current user data has been loaded successfully'
          .format(current_user.username, username))
    logger.info('Current User: {}\n'
                '\t\tCASE - <cases/{}>: current user data has been loaded successfully'
                .format(current_user.username, username))
    current_user_cases_and_groups = CaseMethod.get_user_cases_and_groups_by_username(username)
    
    if current_user_cases_and_groups:
        print('Current User: {}\n'
              '\t\tCASE - <cases/{}>: current_user_cases_and_groups loaded successfully'
              .format(current_user.username, username))
        logger.info('Current User: {}\n'
                    '\t\tCASE - <cases/{}>: current_user_cases_and_groups loaded successfully'
                    .format(current_user.username, username))
    else:
        print('Current User: {}\n'
              '\t\tCASE - <cases/{}>: current_user_cases_and_groups could not be loaded'
              .format(current_user.username, username))
        logger.warning('Current User: {}\n'
                       '\t\tCASE - <cases/{}>: current_user_cases_and_groups could not be loaded'
                       .format(current_user.username, username))
    
    print('current_user_cases_and_groups: ', current_user_cases_and_groups)
    
    return render_template('case/case_user_cases.html',
                           cases=current_user_cases_and_groups,
                           language_class='flag-icon-co' if session['language'] == 'es' else 'flag-icon-us',
                           profile=current_user.profile,
                           state=request.args.get('state'),
                           title='User Cases')


@case_bp.route('/cases/user/login')
@login_required
def cases_user_login ():
    print('------------------ case_bp.route(/cases/user/login)')
    current_user_username = current_user.username
    logger = init_logger(__name__, testing_mode=False)
    logger.info('Current User: {}\n'
                '\t\tCASE - <cases/user/login>: current user username: {}'
                .format(current_user.username, current_user_username))
    print('current_user_username: ', current_user_username)
    
    return redirect(url_for('case_bp.cases_user',
                            state=request.args.get('state'),
                            username=current_user_username))


@case_bp.route('/case/detail/<case_name>')
@login_required
def case_detail (case_name: str):
    print('------------------- case_bp.route(/case/detail/{})'.format(case_name))
    # Show all case data, and allows to add information (objects + meta-data) to case
    return None


@case_bp.route('/case/create/', methods=['POST'])
@login_required
def create():
    # Case create
    print('----------------- case_bp.route(/case/create/) - {}'.format(request.method))
    logger = init_logger(__name__, testing_mode=False)
    profile = session['profile']
    currentUserUsername = current_user.username
    # if request.method == 'POST':
    caseId = request.form.get('id')
    caseGroup = request.form.get('group')
    caseName = request.form.get('name')
    caseDescription = request.form.get('description')
    caseType = request.form.get('type')
    caseStatus = request.form.get('status')
    caseDueDate = request.form.get('dueDate')
    caseClientName = request.form.get('clientName')
    caseClientId = request.form.get('clientId')
    caseClientDescription = request.form.get('clientDescription')
    validateExistUser = CaseMethod.validate_case_exist(caseId)
    print('validate_exist_user: ', validateExistUser.count())
    print('*** --- caseGroup: ', caseGroup)
    
    # Validate if case_id does not exist
    if validateExistUser.count() == 0:
        print('case with ID: {} - does not exist...'.format(caseId))
        newCase = {'id': caseId,
                   'name': caseName,
                   'description': caseDescription,
                   'type': caseType,
                   'status': caseStatus,
                   'groups': [caseGroup],
                   'due_date': caseDueDate,
                   'client_name': caseClientName,
                   'client_id': caseClientId,
                   'client_description': caseClientDescription}
        print('NEW CASE - data: {}'.format(newCase))
        caseCreated = CaseMethod.create_case(newCase)
        if caseCreated:
            flash('Case created successfully')
            logger.info('Current User: {}\n'
                        '\t\tCASE - <create - POST>: Case \'{}\' has been created successfully'
                        .format(current_user.username, caseName))
        else:
            flash('Case could not be created...')
            logger.warning('Current User: {}\n'
                           '\t\tCASE - <create - POST>: Case \'{}\' could not be created'
                           .format(current_user.username, caseName))
    else:
        print('Provided case ID already exist...')
        flash('Case could not be created... Provided case ID already exist')
        logger.warning('Current User: {}\n'
                       '\t\tCASE - <create - POST>: Case \'{}\' could not be created'
                       .format(current_user.username, caseId))
    return redirect(url_for('case_bp.cases_user',
                            state=request.args.get('state'),
                            username=currentUserUsername))


@case_bp.route('/case/delete/<case_name>')
@login_required
def delete (case_name: str):
    # Case delete
    print('----------------- case_bp.route(/case/delete/)')
    print('case_name: ', case_name)
    logger = init_logger(__name__, testing_mode=False)
    profile = session['profile']
    delete_case = CaseMethod.delete_case_by_case_name(case_name)
    if delete_case:
        flash('The case <{}> has been deleted successfully'.format(case_name))
        logger.info('Current User: {}\n'
                    '\t\tCASE - <delete>: case \'{}\' has been deleted successfully'
                    .format(current_user.username, case_name))
    else:
        flash('The case <{}> could not be deleted'.format(case_name))
        logger.warning('Current User: {}\n'
                       '\t\tCASE - <delete>: case \'{}\' could not be deleted'
                       .format(current_user.username, case_name))
    return redirect(url_for('case_bp.cases',
                            profile=profile))


@case_bp.route('/case/read/<case_name>')
@login_required
def read (case_name: str):
    # Case read
    print('----------------- case_bp.route(/case/read/)')
    print('case_name: ', case_name)
    logger = init_logger(__name__, testing_mode=False)
    profile = session['profile']
    case_data = CaseMethod.get_case_by_case_name(case_name)
    groups = CaseMethod.get_all_groups_name()
    if case_data:
        logger.info('Current User: {}\n'
                    '\t\tCASE - <read>: case_data loaded successfully - case_name: {}'
                    .format(current_user.username, case_data['name']))
    else:
        logger.warning('Current User: {}\n'
                       '\t\tCASE - <read>: case_data could not be loaded'
                       .format(current_user.username))
    if groups:
        logger.info('Current User: {}\n'
                    '\t\tCASE - <read>: groups loaded successfully - groups len: {}'
                    .format(current_user.username, len(groups)))
    else:
        logger.warning('Current User: {}\n'
                       '\t\tCASE - <read>: groups could not be loaded'
                       .format(current_user.username))
    print('case_data: ', case_data)
    print('groups: ', groups)
    return render_template('case/case_read.html',
                           case=case_data,
                           groups=groups,
                           profile=profile)


@case_bp.route('/case/update/<case_name>', methods=['GET', 'POST'])
@login_required
def update (case_name: str):
    # Case update
    print('----------------- case_bp.route(/case/update/) - {}'.format(request.method))
    print('case_name: ', case_name)
    logger = init_logger(__name__, testing_mode=False)
    profile = session['profile']
    if request.method == 'GET':
        case_data = CaseMethod.get_case_by_case_name(case_name)
        print('case_data: ', case_data)
        if case_data:
            print('CASE - <update - GET>: case_data loaded successfully - case_name: {}'.format(case_data['name']))
            logger.info('Current User: {}\n'
                        '\t\tCASE - <update - GET>: case_data loaded successfully - case_name: {}'
                        .format(current_user.username, case_data['name']))
        else:
            logger.error('Current User: {}\n'
                         '\t\tCASE - <update - GET>: case_data could not be loaded'
                         .format(current_user.username))
        all_groups = CaseMethod.get_all_groups_name()
        if all_groups and len(all_groups) > 0:
            logger.info('Current User: {}\n'
                        '\t\tCASE - <update>: all_groups loaded successfully - all_groups len: {}'
                        .format(current_user.username, len(all_groups)))
        else:
            logger.error('Current User: {}\n'
                         '\t\tCASE - <update - GET>: all_groups could not be loaded'
                         .format(current_user.username))
        print('case_data: ', case_data)
        print('all_groups: ', all_groups)
        all_groups = CaseMethod.filter_groups(all_groups, case_data['groups'])
        print('*** all_groups: ', all_groups)
        return case_data
        # return render_template('case/case_update.html',
        #                case=case_data,
        #                groups=all_groups,
        #                profile=profile)
    elif request.method == 'POST':
        groups = request.form.getlist('current_case_groups')
        case_data = {
            'name': request.form.get('name'),
            'description': request.form.get('description'),
            'groups': groups
        }
        print('case_data: ', case_data)
        print('case_name: ', case_name)
        if CaseMethod.update_case_data(case_name, case_data):
            logger.info('Current User: {}\n'
                        '\t\tCASE - <update - POST>: Case \'{}\' updated successfully'
                        .format(current_user.username, case_data['name']))
        else:
            logger.warning('Current User: {}\n'
                           '\t\tCASE - <update - POST>: Case \'{}\' could not be updated'
                           .format(current_user.username, case_data['name']))
    return redirect(url_for('case_bp.cases',
                            profile=profile))
