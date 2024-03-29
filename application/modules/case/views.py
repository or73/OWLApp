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
import xlrd
from _datetime import datetime

from .methods import CaseMethod

from application.modules import init_logger

case_bp = Blueprint('case_bp', __name__)


# --------------------------------------- cases
@case_bp.route('/case/<caseName>')
@login_required
def case_environment(caseName: str):
    # Create case environment
    print('------------------- case_bp.route(/case/{})'.format(caseName))
    logger = init_logger(__name__, testing_mode=False)
    logger.info('Current User: {}\n'
                '\t\tCASE - <case_environment>: The case <{}> has been selected'
                .format(current_user.username, caseName))
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
    """
    Call CaseMethod methods to retrieve some information:
    - get_all_cases_name_id: retrieve a list of dict {'name': <case_name>, 'caseId': <caseId>}
    - get_all_groups_name: retrieve a list of dict {'name': <group_name>}
    From each list of dicts, a new list is created containing only strings>
    - casesIdList: list of all cases ID
    - casesNameList: list of all cases name
    - groupsLIst> list of all groups name
    :return: dict containing all different groups name
    """
    print('----------------- case_bp.route(/cases/allGroups/)')
    allGroupsName = CaseMethod.get_all_groups_name()
    allCasesIdAndName = CaseMethod.get_all_cases_name_id()
    
    print('allGroupsName: ', allGroupsName)
    casesIdList = []
    casesNameList = []
    groupsList = []
    
    # Create a couple of lists containing casesId and casesName
    for case in allCasesIdAndName:
        casesIdList.append(case['caseId'])
        casesNameList.append(case['name'])
    
    # Create a list containing only unique groups name
    for group in allGroupsName:
        groupsList.append(group['name'])
    print('groupsList: ', groupsList)
    return {
        'casesIdList': casesIdList,
        'casesNameList': casesNameList,
        'groupsList': groupsList
    }


@case_bp.route('/cases/allCasesNameId/')
@login_required
def allGroupsAndCases():
    print('------------------ allGroupsAndCases </cases/allCasesNameId/>')
    return CaseMethod.get_all_cases_name_id()


@case_bp.route('/case/file/', methods=['POST'])
@login_required
def caseFile():
    print('--------------------- caseFile </case/file/>')
    casesList = request.get_json()
    toReturn = CaseMethod.setClassToExcelFile(casesList)
    return toReturn


@case_bp.route('/case/upload/file/', methods=['POST'])
@login_required
def caseUploadFile():
    print('-------------------- caseUploadFile </case/upload/file>')
    print('request: ', request)
    print('request.files: ', request.files)
    caseFileData = request.files['caseFile'].read()
    # print('caseFileData: ', caseFileData)
    # Open .xls/.xlsx file and validate data
    workbook = xlrd.open_workbook(filename='format.xlsx', file_contents=caseFileData)
    sheet = workbook.sheet_by_index(0)   # 1st sheet
    print('sheet(2,1): ', sheet.cell_value(2, 1))
    print('sheet(14, 2): ', sheet.cell_value(14, 2))
    print('type(sheet(14, 2)): ', type(sheet.cell_value(14, 2)))
    print('datetime(sheet(14, 2)): ', (sheet.cell_value(14, 2)).strip().replace(' ', 'T') + ':00')
    caseData = dict(id=sheet.cell_value(3, 2),
                    name=sheet.cell_value(4, 2),
                    description=sheet.cell_value(5, 2),
                    status=sheet.cell_value(7, 1),
                    type=sheet.cell_value(7, 2),
                    groups=sheet.cell_value(8, 2),
                    clientId=sheet.cell_value(10, 2),
                    clientName=sheet.cell_value(11, 2),
                    creationDate=sheet.cell_value(13, 2),
                    dueDate=(sheet.cell_value(14, 2)).strip().replace(' ', 'T') + ':00',
                    lastModification=sheet.cell_value(15, 2),
                    )
    return CaseMethod.create_case(caseData)


@case_bp.route('/cases/<username>')
@login_required
def cases_user(username: str):
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
def cases_user_login():
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


@case_bp.route('/case/detail/<caseName>')
@login_required
def case_detail(caseName: str):
    print('------------------- case_bp.route(/case/detail/{})'.format(caseName))
    # Show all case data, and allows to add information (objects + meta-data) to case
    return None


@case_bp.route('/case/create/', methods=['POST'])
@login_required
def create():
    # Case create
    print('----------------- case_bp.route(/case/create/) - {}'.format(request.method))
    logger = init_logger(__name__, testing_mode=False)
    # profile = session['profile']
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
    
    # Validate if caseId does not exist
    if validateExistUser.count() == 0:
        print('case with ID: {} - does not exist...'.format(caseId))
        newCase = {'id': caseId,
                   'name': caseName,
                   'description': caseDescription,
                   'type': caseType,
                   'status': caseStatus,
                   'groups': [caseGroup],
                   'dueDate': caseDueDate,
                   'clientName': caseClientName,
                   'clientId': caseClientId,
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


@case_bp.route('/case/delete/<caseName>', methods=['POST'])
@login_required
def delete(caseName: str):
    # Case delete
    print('----------------- case_bp.route(/case/delete/)')
    print('caseName: ', caseName)
    logger = init_logger(__name__, testing_mode=False)
    # profile = session['profile']
    delete_case = CaseMethod.delete_case_by_case_name(caseName)
    if delete_case:
        flash('The case <{}> has been deleted successfully'.format(caseName))
        logger.info('Current User: {}\n'
                    '\t\tCASE - <delete>: case \'{}\' has been deleted successfully'
                    .format(current_user.username, caseName))
    else:
        flash('The case <{}> could not be deleted'.format(caseName))
        logger.warning('Current User: {}\n'
                       '\t\tCASE - <delete>: case \'{}\' could not be deleted'
                       .format(current_user.username, caseName))
    return redirect(url_for('case_bp.cases_user',
                            username=current_user.username))


@case_bp.route('/case/read/<caseName>')
@login_required
def read(caseName: str):
    # Case read
    print('----------------- case_bp.route(/case/read/)')
    print('caseName: ', caseName)
    logger = init_logger(__name__, testing_mode=False)
    # profile = session['profile']
    case_data = CaseMethod.get_case_by_case_name(caseName)
    groups = CaseMethod.get_all_groups_name()
    if case_data:
        logger.info('Current User: {}\n'
                    '\t\tCASE - <read>: case_data loaded successfully - caseName: {}'
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
    return case_data
    # return render_template('case/case_read.html',
    #                        case=case_data,
    #                        groups=groups,
    #                        profile=profile)


@case_bp.route('/case/update/<caseName>', methods=['GET', 'POST'])
@login_required
def update(caseName: str):
    # Case update
    print('----------------- case_bp.route(/case/update/) - {}'.format(request.method))
    print('caseName: ', caseName)
    logger = init_logger(__name__, testing_mode=False)
    # profile = session['profile']
    if request.method == 'GET':
        case_data = CaseMethod.get_case_by_case_name(caseName)
        print('case_data: ', case_data)
        if case_data:
            print('CASE - <update - GET>: case_data loaded successfully - caseName: {}'.format(case_data['name']))
            logger.info('Current User: {}\n'
                        '\t\tCASE - <update - GET>: case_data loaded successfully - caseName: {}'
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
        # groups = request.form.getlist('current_case_groups')
        case_data = {
            'name': request.form.get('name'),
            'caseId': request.form.get('id'),
            'description': request.form.get('description'),
            'groups': [request.form.get('group')],
            'status': request.form.get('status'),
            'type': request.form.get('type'),
            'dueDate': request.form.get('dueDate')
        }
        print('case_data: ', case_data)
        print('caseName: ', caseName)
        if CaseMethod.update_case_data(caseName, case_data):
            logger.info('Current User: {}\n'
                        '\t\tCASE - <update - POST>: Case \'{}\' updated successfully'
                        .format(current_user.username, case_data['name']))
        else:
            logger.warning('Current User: {}\n'
                           '\t\tCASE - <update - POST>: Case \'{}\' could not be updated'
                           .format(current_user.username, case_data['name']))
    return redirect(url_for('case_bp.cases_user',
                            username=current_user.username))
