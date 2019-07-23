"""
File Path: application/modules/group/methods.py
Description: Group methods for App - Define Group methods
Copyright (c) 2019. This Application has been developed by OR73.
"""
from typing import Union
from application.setup import mongo
from .models import Group

from ..user import UserMethod


class GroupMethod(Group):
    @staticmethod
    def user_add_group_managers(managers: list, group_name: str) -> bool:
        # Mark users as group manager
        return UserMethod.add_group_managers(managers, group_name)

    @staticmethod
    def user_add_group_users(users: list, group_name: str) -> bool:
        # Mark users as member of a group
        return UserMethod.add_group_users(users, group_name)

    @staticmethod
    def create_group(group: dict) -> Union[Group, bool]:
        print('---------------- create_group - ', group)
        groups_collection = mongo.db.groups
        # Create a new group
        # Validate that group does not exist
        new_group = groups_collection.find({'name': group['name']})
        print('new_group: ', new_group)
        print('dict(new_group): ', dict(new_group))
        # Validate that group does not exist
        if new_group.count() == 0 or not new_group:
            print('Group does not exist: ', group)
            new_group = Group(group)
            print('new_group: ', new_group)
            if len(group['user_groups_manager']) > 0:
                GroupMethod.user_add_group_managers(group['user_groups_manager'], group['name'])
            if len(group['user_groups']) > 0:
                GroupMethod.user_add_group_users(group['user_groups'], group['name'])
            mongo.db.groups.insert_one(new_group.serialize)
            return new_group
        return False

    @staticmethod
    def delete_group(group_name: str) -> bool:
        # Delete a group
        return mongo.db.groups.delete_one({'name': group_name})

    @staticmethod
    def delete_group_by_group_name(group_name: str) -> bool:
        # Delete a group by its group_name
        groups_collection = mongo.db.groups
        validate_group = groups_collection.find({'name': group_name})
        if validate_group.count() > 0:
            # Delete group
            groups_collection.delete_one({'name': group_name})
            return True
        return False

    @staticmethod
    def extract_managers_and_users(all_users_list: list, managers_list: list, users_list: list) -> list:
        # Extract all current users of managers_list and users_list from all_users_list
        print('all_users_list: ', all_users_list)
        print('managers_list: ', managers_list)
        print('users_list: ', users_list)
        reduced_list = []
        for user in all_users_list:
            if user not in managers_list and user not in users_list:
                reduced_list.append(user)
        return reduced_list

    @staticmethod
    def extract_users(users_list: list) -> list:
        # Take a list and extract a user list
        cleaned_users_list = []
        for user in users_list:
            print('user: ', user)
            user_without_space = user.replace(' ', '')
            if '\r' in user_without_space:
                first_user_string = user_without_space.split('\r')[1]
                print('first_user_string: ', first_user_string)
                cleaned_user = first_user_string[1:]
                print('cleaned_user: ', cleaned_user)
                cleaned_users_list.append(cleaned_user)
            else:
                cleaned_users_list.append(user)

        print('cleaned_users_list: ', cleaned_users_list)
        return cleaned_users_list

    @staticmethod
    def get_all_groups() -> list:
        groups_collection = mongo.db.groups
        # Return all group in DB
        return list(groups_collection.find({}))

    @staticmethod
    def get_all_group_names() -> list:
        # Return a list of group names
        groups_collection = mongo.db.groups
        return list(groups_collection.find({}, {'_id': 0, 'name': 1}))

    @staticmethod
    def get_group_by_group_name(group_name: str) -> Union[Group, bool]:
        # Return all group_data by its group_name
        print('--------------------- get_group_by_group_name - {}'.format(group_name))
        groups_collection = mongo.db.groups
        group_by_name = groups_collection.find_one({'name': group_name})
        if group_by_name:
            print('Group already exist')
            return group_by_name
        print('Group does not exist')
        return False

    @staticmethod
    def only_username_list(full_list: list) -> list:
        # Extract each username from full_list and return a list with username
        print('full_list: ', full_list)
        username_list = []
        for item in full_list:
            username_list.append(item['username'])
        print('username_list: ', username_list)
        return username_list

    @staticmethod
    def read_group(group_name: str) -> dict:
        # Read a group by its name
        return mongo.db.groups.find({'name': group_name})

    @staticmethod
    def update_group_data(group_name: str, group_data: dict) -> Union[Group, bool]:
        groups_collection = mongo.db.groups
        # Update group data
        group_update = groups_collection.update_one({'name': group_name},
                                                    {'$set': {'name': group_data['name'],
                                                              'description': group_data['description'],
                                                              'managers': group_data['manager'],
                                                              'users': group_data['user']}})
        if group_update:
            print('group_update: ', group_update)
            return group_update
        print('Group could not be updated')
        return False

    # ------------------------ users
    @staticmethod
    def user_get_all_groups_manager(username: str) -> list:
        # Return a list of groups in which username is manager
        user = UserMethod.get_user_by_username(username)
        groups_collection = mongo.db.groups
        print('----------------- user_get_all_groups_manager - ', username)
        # Get all groups of specified user
        groups = user['user_groups_manager']
        groups_list = []
        # Get group Object and add it to a list
        for group_name in groups:
            group = groups_collection.find_one({'name': group_name})
            groups_list.append(group)
        return groups_list

    @staticmethod
    def users_get_all_users_username() -> list:
        # Return a username list of user from DB
        return UserMethod.get_all_users_username()

    @staticmethod
    def users_get_all_users_username_manager(username: str) -> list:
        # Return a list of users' username in which a provided username is manager
        return UserMethod.get_all_users_name_manager(username)
