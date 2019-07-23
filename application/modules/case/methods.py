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
        validate_case = cases_collection.find({'name': case_data['name']})
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
        users_collection = mongo.db.users
        user = users_collection.find_one({'username': username})
        print('user: ', user)
        user_groups_manager = []
        user_groups = []

        if 'user_groups_manager' in user:
            user_groups_manager = user['user_groups_manager']
        if 'user_groups' in user:
            user_groups = user['user_groups']
        print('user_groups_manager: ', user_groups_manager)
        print('user_groups: ', user_groups)

        cases_collection = mongo.db.cases
        all_cases = cases_collection.find()
        print('all_cases: ', all_cases)

        user_groups_manager_dict = {}
        user_groups_dict = {}
        for case in all_cases:
            new_case = {'name': case['name'],
                        'description': case['description'],
                        'creation_date': (case['creation_date']).strftime('%A, %d-%B-%Y %I:%M%p')}
            for group in case['groups']:
                print('????????????????????\n'
                      '\tcase: {}\n'
                      '\tgroup: {}\n'
                      '\tuser_groups_manager: {}\n'
                      '\tuser_groups: {}\n'
                      '????????????????????'.format(case, group, user_groups_manager, user_groups))
                if group in user_groups_manager:
                    print('*** MANAGWE *** group {} is a groups_manager'.format(group))
                    user_groups_manager_dict[group] = new_case
                elif group in user_groups:
                    print('*** USER *** group {} is a groups_user'.format(group))
                    user_groups_dict[group] = new_case
                print('user_groups_manager_dict: {}'.format(user_groups_manager_dict))
                print('user_groups_dict: {}'.format(user_groups_dict))
        user_data_to_return = {'manager': user_groups_manager_dict,
                               'user': user_groups_dict}
        print('user_data_to_return: ', user_data_to_return)
        return user_data_to_return

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
