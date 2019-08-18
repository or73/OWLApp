"""
File Path: application/modules/case/methods.py
Description: Case methods for App - Define Case methods
Copyright (c) 2019. This Application has been developed by OR73.
"""
from typing import Union
from application.setup import mongo
from .models import Case


class CaseMethod(Case):
    @staticmethod
    def create_case(case_data: dict) -> Union[dict, bool]:
        # Validate that case does not exist
        print('-------------------- create_case - {}'.format(case_data))
        print('type(case_data): ', type(case_data))
        print('case_data[name]: ', case_data['name'])
        cases_collection = mongo.db.cases
        validate_case = cases_collection.find({'case_id': case_data['id']})
        print('validate_case.count', validate_case.count())
        if validate_case.count() == 0:
            print('Case does not exist: {}'.format(case_data['name']))
            # Create a new case
            new_case = Case(case_data)
            print('new_case: ', new_case)
            cases_collection.insert_one(new_case.serialize)
            return new_case.serialize
        return False

    @staticmethod
    def delete_case_by_case_name(case_name: str) -> bool:
        print('---------------- delete_case_by_case_name {}'.format(case_name))
        # Delete a case by its case_name
        validate_case = mongo.db.cases.find({'name': case_name})
        if validate_case.count() > 0:
            print('Case \'case_name\': {} has been found in DB'.format(case_name))
            # Delete Case
            cases_collection = mongo.db.cases
            delete_case = cases_collection.delete_one({'name': case_name})
            print('delete_case: ', delete_case)
            # print('delete_case.count: ', delete_case.count)
            print('delete_case.delete_count: ', delete_case.deleted_count)
            if delete_case.deleted_count > 0:
                print('Case \'{}\' has been deleted successfully'.format(case_name))
                return True
            else:
                print('1. Case {} could not be deleted'.format(case_name))
                return False
        print('2. Case {} could not be deleted'.format(case_name))
        return False

    @staticmethod
    def filter_groups(all_groups: list, case_groups: list) -> list:
        # Compare both lists and create a new list without case_group cases
        case_groups_list = []
        for group in all_groups:
            if group['name'] not in case_groups:
                case_groups_list.append(group['name'])
        print('case_group_list: ', case_groups_list)
        return case_groups_list

    @staticmethod
    def get_all_cases() -> list:
        print('---------------- get_all_cases')
        # Return all cases from DB
        cases_collection = mongo.db.cases
        return list(cases_collection.find({}, {'_id': 0}))

    @staticmethod
    def get_all_groups_name() -> list:
        # Return a list of all groups' names
        # return list(GroupMethod.get_all_group_names())
        print('------------------ get_all_groups_name')
        groups_collection = mongo.db.groups
        return list(groups_collection.find({}, {'_id': 0, 'name': 1}))

    @staticmethod
    def get_case_by_case_name(case_name: str) -> Union[Case, bool]:
        # Return all case data by its case_name
        print('------------------- get_case_by_case_name: ', case_name)
        cases_collection = mongo.db.cases
        case_by_name = cases_collection.find_one({'name': case_name})
        if case_by_name:
            print('Case exists')
            return case_by_name
        print('Case does not exist')
        return False

    @staticmethod
    def get_user_cases_and_groups_by_username(username: str) -> dict:
        # Return all cases associated with username
        print('------------------- get_user_cases_and_groups_by_username: -', username, '-')
        # Load user data
        users_collection = mongo.db.users
        user = users_collection.find_one({'username': username})
        print('user: ', user)
        user_groups_manager = []
        user_groups = []

        # If user has user_groups_manager list, then assign user['user_groups_manager']
        if 'user_groups_manager' in user:
            user_groups_manager = user['user_groups_manager']
        # If user has user_groups list, then assign user['user_groups']
        if 'user_groups' in user:
            user_groups = user['user_groups']
        print('user_groups_manager: ', user_groups_manager)
        print('user_groups: ', user_groups)

        # Load all cases
        cases_collection = mongo.db.cases
        all_cases = cases_collection.find()
        if all_cases:
            print('all_cases have been loaded successfully')
        else:
            print('Something wrong and cases could not be loaded')
            return {}

        user_groups_dict = {}
        counter = 1
        # Search in all_cases
        for case in all_cases:
            print('----------------> {}. case: {}'.format(counter, case))
            counter += 1
            new_case = {'case_id': case['case_id'],
                        'client_id': case['client_id'],
                        'client_name': case['client_name'],
                        'description': case['description'],
                        'groups': {},
                        'name': case['name'],
                        'status': case['status'],
                        'type': case['type'],
                        'creation_date': (case['creation_date']).strftime('%A, %d-%B-%Y %I:%M%p'),
                        'due_date': (case['due_date']).strftime('%A, %d-%B-%Y %I:%M%p'),
                        'last_update': (case['last_modification']).strftime('%A, %d-%B-%Y %I:%M%p')}
            print('-*-*-*-*-*-*-*-*-*-* {}. new_case: '.format(counter, new_case))

            if len(user_groups) == 0 and len(user_groups_manager) == 0:
                new_case['groups'] = {}
                user_groups_dict[case['name']] = new_case
            else:
                # Compare each case-group
                for group in case['groups']:
                    print('????????????????????\n'
                          '\tcase: {}\n'
                          '\tgroup: {}\n'
                          '\tuser_groups_manager: {}\n'
                          '\tuser_groups: {}\n'
                          '????????????????????'.format(case, group, user_groups_manager, user_groups))
                    if group in user_groups_manager or group in user_groups:
                        if case['name'] not in user_groups_dict:
                            # if group is into user_groups_manager elif group is into user_groups
                            new_case['groups'][group] = {'role': 'Admin'} \
                                if (group in user_groups_manager) \
                                else {'role': 'User'}
                            user_groups_dict[case['name']] = new_case
                        else:
                            user_groups_dict[case['name']]['groups'][group] = {'role': 'Admin'} \
                                if (group in user_groups_manager) \
                                else {'role': 'User'}
                print('1. user_groups_dict: {}'.format(user_groups_dict))
        print('2. user_groups_dict: {}'.format(user_groups_dict))
        return user_groups_dict

    @staticmethod
    def update_case_data(case_name: str, case_data: dict) -> bool:
        # Update case data
        print('------------------ update_case_data')
        cases_collection = mongo.db.cases
        case_update = cases_collection.update({'name': case_name},
                                              {'$set': {'name': case_data['name'],
                                                        'description': case_data['description'],
                                                        'groups': case_data['groups']}})
        if case_update:
            print('case_update: ', case_update)
            return True
        return False

    @staticmethod
    def validate_case_exist(case_id):
        # Validate if a provided case_id exists or not in DB
        print('--------------------- validate_case_exist')
        cases_collection = mongo.db.cases
        return cases_collection.find({'case_id': case_id})
