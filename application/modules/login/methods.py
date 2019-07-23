"""
File path: application/modules/login/methods.py
Description: Auth methods for App - Define login data methods
Copyright (c) 2019. This Application has been developed by OR73.
"""
import datetime
import random
import string
from typing import Union
from .models import Login
from ..user import (User, UserMethod)
from application.setup import mongo


class LoginMethod:
    @staticmethod
    def create_login(user_id) -> bool:
        # create a register in the database for login session
        print('----------------- create_login - user_id: ', user_id)
        # Create new login session register
        new_login = Login(user_id=user_id)
        if new_login:
            print('new_login: ', new_login)
            mongo.db.logins.insert_one(new_login.serialize)
            return True
        print('New login could not be created...')
        return False

    @staticmethod
    def dump_datetime(value) -> str:
        # Deserialize datetime object into string form from JSON processing
        if value is None:
            return ''
        return value.strftime('%Y-%m%d %H:%M:%S')

    @staticmethod
    def generate_state_var() -> str:
        # Generate state variable
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=32))

    @staticmethod
    def get_user_by_email(email: str) -> object:
        # create new user
        user_by_email = UserMethod.get_user_by_email(email)
        print('user_by_email: ', user_by_email)
        """ Retrieve a user data with a provided email """
        if user_by_email:
            return user_by_email
        else:
            return False

    @staticmethod
    def get_user_email_by_email_or_username(email_or_username: str) -> Union[str, bool]:
        # Validate if provided string is email or not, and find user email
        print('-------------- get_user_email_by_email_or_username: ', email_or_username)
        email = UserMethod.get_user_by_email(email_or_username)
        print('1. email: ', email)
        if email:
            print('An email has been provided for validation')
            return email
        email = UserMethod.get_user_by_username(email_or_username)
        if email:
            print('An username has been provided for validation')
            return email['email']
        return False

    @staticmethod
    def update_logout_time(user_id: str) -> None:
        # Update logout time for current session
        mongo.db.logins.update({'user_id': user_id}, {'$set': {'logout_time': datetime.datetime.utcnow()}})

    @staticmethod
    def user_method_get_user_id(user) -> str:
        # Return user_id of a provided user
        return UserMethod.get_user_id(user)

    @staticmethod
    def user_method_session_data(user, state) -> dict:
        # Return an object with current user data to update user session
        return UserMethod.session_data(user, state)

    @staticmethod
    def user_method_validate_user(user_from_db_by_email, password) -> Union[User, None]:
        # Validate if a user exists with a provided email
        user = UserMethod.validate_user(user_from_db_by_email)
        if user:
            if UserMethod.validate_password(user, password) and UserMethod.validate_user_active(user):
                return user
        return None
