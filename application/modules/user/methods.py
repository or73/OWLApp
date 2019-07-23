"""
File Path: application/modules/user/methods.py
Description: User methods for App - Define User methods
Copyright (c) 2019. This Application has been developed by OR73.
"""
from flask_login import current_user
from typing import Union
from application.setup import (login_manager, mongo)
from .models import User


# from ..case import CaseMethod


def validate_user_email(email: str) -> bool:
    # Validate if a user exist with a provided email
    print('--------------------- validate_user_email - ', email)
    users_collection = mongo.db.users
    user_email_validation = users_collection.find_one({'email': email})
    # exist_user = User.objects(email=email).first()
    print('user_email_validation: ', user_email_validation)
    if not user_email_validation or user_email_validation['email'] != email:
        print('return False')
        return False  # User email does not exist
    print('return True')
    return True  # User email already exist


class UserMethod:
    # ------------------------------ User
    @staticmethod
    def add_group_managers(managers: list, group_name: str) -> bool:
        users_collection = mongo.db.users
        # Mark users as managers
        for manager in managers:
            user_find_and_update = users_collection.find_one_and_update({'username': manager,
                                                                         'users_group_manager': {'$ne': group_name}},
                                                                        {'$push': {'users_group_manager': group_name}})
            print('user_find_and_update: ', user_find_and_update)
        return True

    @staticmethod
    def add_group_users(users: list, group_name: str) -> bool:
        users_collection = mongo.db.users
        # Mark users as member of group
        print('add_group_users: ')
        for user in users:
            user_find_and_update = users_collection.find_one_and_update({'username': user,
                                                                         'users_group': {'$ne': group_name}},
                                                                        {'$push': {'users_group': group_name}})
            print('user_find_and_update: ', user_find_and_update)

        return True

    @staticmethod
    def create_user(user: dict, picture) -> Union[dict, bool]:
        # Create a new user
        # Return the user object, of the new created user, if the email doesn't exist otherwise return False
        print('------------------- create_user')
        # Validate if user already exist
        if not validate_user_email(email=user['email']):
            print('picture: ', picture)
            mongo.save_file(picture.filename, picture)
            new_user = User(user).serialize
            users_collection = mongo.db.users
            users_collection.insert_one(new_user)
            return new_user
        return False

    @staticmethod
    def delete_user_by_username(username: str) -> bool:
        # Delete an user by its username
        print('------------------- delete_user')
        users_collection = mongo.db.users
        delete_user = users_collection.delete_one({'username': username})
        if delete_user.deleted_count > 0:
            return True
        return False

    @staticmethod
    def get_all_users_name() -> list:
        # Return a list of user's names from DB
        print('------------------- get_all_users_name')
        print('current_user: ', current_user)
        print('current_user[username]: ', current_user.username)
        users_collection = mongo.db.users
        user = users_collection.find_one({'username': current_user.username})
        print('user: ', user)

        all_users_username = list(users_collection.find({'_id': {'$ne': user['_id']}},
                                                        {'_id': 0, 'username': 1,
                                                         'profile': 1, 'session_token': 1,
                                                         'user_groups': 1, 'user_groups_manager': 1}).sort('username'))
        return all_users_username

    @staticmethod
    def get_all_users_username() -> list:
        # Return a list of user's username from DB
        print('-------------------- get_all_users_username')
        users_collection = mongo.db.users
        all_users_username = list(users_collection.find({},
                                                        {'_id': 0, 'profile': 1,
                                                         'user_groups': 1, 'user_groups_manager': 1,
                                                         'username': 1})
                                  .sort('username'))
        return all_users_username

    @staticmethod
    def get_all_users_name_manager(username: str) -> list:
        # Return a list of user's username from DB, of an specified manager
        print('-------------------- gel_all_users_name_manager -{}-'.format(username))
        users_collection = mongo.db.users
        groups_collection = mongo.db.groups
        # Load groups in which username is manager
        user = users_collection.find_one({'username': username},
                                         {'_id': 0, 'user_groups_manager': 1})
        print('user: ', user)
        user_groups = user['user_groups_manager']
        print('user_groups: ', user_groups)
        print('type(user_groups): ', type(user_groups))
        # Load all users of each group, in which username is manager
        all_users_username = []
        for group in user_groups:
            print('group: ', group)
            users = groups_collection.find_one({'name': group},
                                               {'_id': 0, 'users': 1})
            all_users_username = all_users_username + users['users']
            print('all_users: ', all_users_username)
        # Load each user information to return
        to_return = []
        revised_user = []
        for username in all_users_username:
            if username not in revised_user:
                one_user = users_collection.find_one({'username': username},
                                                     {'_id': 0, 'profile': 1,
                                                      'user_groups': 1, 'user_groups_manager': 1,
                                                      'username': 1})
                to_return.append(one_user)
            # Validate that a user is added only once
            revised_user.append(username)
        # Return all users in which username is manager
        print('all_users to return: ', to_return)
        return to_return

    @staticmethod
    def get_id_by_session_token(session_token) -> str:
        users_collection = mongo.db.users
        # Return user_id of a provided session_token
        user = users_collection.find_one({'session_token': session_token})
        return user.id

    @staticmethod
    def get_user_id(user: User) -> str:
        # Return user_id
        return user.get_id()

    @staticmethod
    def get_user_by_email(email: str) -> Union[dict, bool]:
        users_collection = mongo.db.users
        # Return a user by email
        print('------------------ get_user_by_email')
        user = users_collection.find_one({'email': email})
        print('user: ', user)
        if user:
            return user
        return False

    @staticmethod
    def get_user_by_session_data(session_data) -> Union[dict, bool]:
        users_collection = mongo.db.users
        # Return a user, without _id
        print('------------------ get_user_by_session_data')
        user = users_collection.find_one({'username': session_data},
                                         {'_id': 0, 'last_login': 0, 'authenticated': 0,
                                          'session_token': 0})
        print('user |---: ', user)
        if user:
            return user
        return False

    @staticmethod
    def get_user_by_username(username: str) -> Union[dict, bool]:
        # Return a User object by a provided username
        users_collection = mongo.db.users
        print('-----------------  get_user_by_username - ', username)
        user = users_collection.find_one({'username': username})
        if user:
            return user
        return False

    @login_manager.user_loader
    def load_user(session_token: str) -> User:
        users_collection = mongo.db.users
        # Return a user by user_id
        print('------------------ load_user')
        user = users_collection.find_one({'session_token': session_token})
        return User(user)

    @staticmethod
    def load_user_picture(filename: str):
        print('------------------ load_user_picture')
        print('mongo.send_file(filename): ', mongo.send_file(filename))
        return mongo.send_file(filename)

    @staticmethod
    def session_data(user: User, state: str) -> dict:
        # Return an object with current user data to update user session
        return {
            'access_token': user.session_token,
            'authenticated': user.authenticated,
            'email': user.email,
            'groups': user.user_groups,
            'language': user.language,
            'manager': user.user_groups_manager,
            'password': user.password_hash,
            'profile': user.profile,
            'provider': user.provider,
            'session_id': state,
            'username': user.username
        }

    @staticmethod
    def update_user_data(profile: str, username: str, user_data: dict, picture=None) -> bool:
        users_collection = mongo.db.users
        # Update user data
        print('------------------ update_user_data - ', user_data)

        if profile == 'admin' and username != current_user.username:
            user_update = users_collection.update_one({'username': username},
                                                      {'$set': {'name': user_data['name'],
                                                                'username': user_data['username'],
                                                                'email': user_data['email'],
                                                                'profile': user_data['profile'],
                                                                'active': False if user_data[
                                                                                       'active'] == 'False' else True}})
        else:
            if picture:
                print('A new user picture has been added')
                mongo.save_file(picture.filename, picture)

            if user_data['password'] != 'Modify Password':
                print('password has been modified')
                user_update = users_collection.update_one({'username': username},
                                                          {'$set': {'name': user_data['name'],
                                                                    'username': user_data['username'],
                                                                    'email': user_data['email'],
                                                                    'language': user_data['language'],
                                                                    'picture': user_data['picture'] if not picture
                                                                    else picture.filename,
                                                                    'password_hash': User.generate_password(user_data['password'])
                                                                    }
                                                           })
            else:
                print('password is the same, it has not been modified ')
                user_update = users_collection.update_one({'username': username},
                                                          {'$set': {'name': user_data['name'],
                                                                    'username': user_data['username'],
                                                                    'email': user_data['email'],
                                                                    'language': user_data['language'],
                                                                    'picture': user_data['picture'] if not picture
                                                                    else picture.filename
                                                                    }
                                                           })
        if user_update:
            print('user_update - user has been updated successfully: ', user_update)
            return True
        print('user_update - user could not be updated')
        return False

    @staticmethod
    def validate_password(user: User, password: str) -> bool:
        # Validate user password
        return user.validate_password(password)

    @staticmethod
    def validate_user(user: dict) -> Union[User, None]:
        # Validate if a user exist in the Database
        print('--------------- validate_user - ', user)
        # Validate if user already exist
        if validate_user_email(user['email']):
            users_collection = mongo.db.users
            print('User validated...')
            user['authenticated'] = True  # Change authenticate boolean to True
            user['provider'] = 'local'  # Set provider as 'Local' user
            users_collection.replace_one({'_id': user['_id']}, user)
            print('user validated and updated: ', user)
            return User(user)
        return None

    @staticmethod
    def validate_user_active(user: User) -> bool:
        # Validate if user is active
        print('---------------- validate_user_active - ', user)
        return user.active

    @staticmethod
    def validate_user_email(email: str) -> bool:
        users_collection = mongo.db.users
        # Validate if email exist in User Collection
        print('validate_user_email: {}'.format(email))
        exist_email = users_collection.find({'email': email})
        print('exist_email: ', exist_email)
        print('exist_email.count: ', exist_email.count)
        if exist_email.count() > 0:
            return True
        return False

    @staticmethod
    def validate_user_username(username: str) -> bool:
        users_collection = mongo.db.users
        # Validate if username exist in User Collection
        print('validate_user_username: {}'.format(username))
        exist_username = users_collection.find({'username': username})
        print('exist_username: ', exist_username)
        print('exist_username.count: ', exist_username.count)
        if exist_username.count() > 0:
            return True
        return False

    # ------------------------------ Case
    @staticmethod
    def case_get_all_cases() -> list:
        # Return all cases from DB
        cases_collection = mongo.db.cases
        return list(cases_collection.find({}, {'_id': 0}))
