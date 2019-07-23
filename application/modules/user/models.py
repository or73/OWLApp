"""
File Path: application/modules/user/models.py
Description: User models for App - Define User models
Copyright (c) 2019. This Application has been developed by OR73.
"""
import datetime
from flask_login import UserMixin
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from werkzeug.security import check_password_hash, generate_password_hash
from application.setup import mongo
from application import Config

profiles = ['admin', 'manager', 'user']


class User(UserMixin):
    def __init__(self, user):
        self.__id = user['_id']
        self.__name = user['name']
        self.__email = user['email']
        self.__password_hash = user['password_hash'] if 'password_hash' in user \
            else generate_password_hash(user['password'])
        self.__profile = user['profile'] if user['profile'] in profiles else 'user'
        self.__provider = user['provider'] if 'provider' in user else 'local'
        self.__session_token = self.generate_token(600)
        self.__username = user['username']
        self.__user_groups = user['user_groups'] if 'user_groups' in user else []
        self.__user_groups_manager = user['user_groups_manager'] if 'user_groups_manager' in user else []
        self.__active = True
        self.__authenticated = False
        self.__last_login = self.set_current_date()
        self.__language = user['language'] if 'language' in user else 'es'
        self.__picture = user['picture']

        # if 'id' in user:
        #     self.id = user['_id']
        if 'session_token' in user:
            self.__session_token = user['session_token']
        if 'active' in user:
            self.__active = user['active']
        if 'authenticated' in user:
            self.__authenticated = user['authenticated']
        if 'last_login' in user:
            self.__last_login = user['last_login']

    # def __repr__(self) -> str:
    #    return '< Username: {}\n name: {}\nEmail: {}\nPassword: {}\nProfile: {}\nProvider: {}\nSessionToken: {}\n' \
    #           'User Groups{}\nUser Groups Manager: {}\nActive: {}\nAuthenticated: {}\nLastLogin: {} >'\
    #        .format(self.__username, self.__name, self.__email, self.__password_hash, self.__profile,
    #                self.provider, self.__session_token, self.__user_groups, self.__user_groups_manager,
    #                self.__active, self.__authenticated, self.__last_login)

    # -------------- getters
    @property
    def serialize(self) -> dict:
        # Return object data in easily serializable format
        return {
            'name': self.__name,
            'username': self.__username,
            'email': self.__email,
            'password_hash': self.__password_hash,
            'profile': self.__profile,
            'provider': self.__provider,
            'session_token': self.__session_token,
            'user_groups': self.__user_groups,
            'user_groups_manager': self.__user_groups_manager,
            'active': self.__active,
            'authenticated': self.__authenticated,
            'last_login': self.__last_login,
            'language': self.__language,
            'picture': self.__picture
        }

    # ---------------------------- properties
    @property
    def active(self) -> bool:
        # Return boolean value to validate if user is active
        return self.__active

    @property
    def authenticated(self) -> bool:
        # Return boolean value to validate if user is authenticated
        return self.__authenticated

    @property
    def id(self) -> int:
        # Return user id
        return self.__id

    @property
    def email(self) -> str:
        # Return user email
        return self.__email

    @property
    def language(self) -> str:
        # Return user language
        return self.__language

    @property
    def last_login(self) -> datetime:
        # Return user last_login date
        return self.__last_login

    @property
    def name(self) -> str:
        # Return user name
        return self.__name

    @property
    def password_hash(self) -> str:
        # Return user password_hash
        return self.__password_hash

    @property
    def picture(self) -> object:
        # Return user picture
        return self.__picture

    @property
    def profile(self) -> str:
        # Return user profile
        return self.__profile

    @property
    def provider(self) -> str:
        # Return user provider
        return self.__provider

    @property
    def session_token(self) -> str:
        # Return user session_token
        return self.__session_token

    @property
    def username(self) -> str:
        # Return user username
        return self.__username

    @property
    def user_groups(self) -> list:
        # Return user_groups list
        return self.__user_groups

    @property
    def user_groups_manager(self) -> list:
        # Return user_groups_manager list
        return self.__user_groups_manager

    # ---------------------------- setters
    @active.setter
    def active(self, new_active: bool) -> None:
        # Update user active status
        self.__active = new_active

    @authenticated.setter
    def authenticated(self, new_authenticated: bool) -> None:
        # Update user authenticated status
        self.__authenticated = new_authenticated

    @id.setter
    def id(self, new_id: str) -> None:
        # Update user_id
        self.__id = new_id

    @email.setter
    def email(self, new_email: str) -> None:
        # Update user email
        self.__email = new_email

    @language.setter
    def language(self, new_language: str) -> None:
        # Update user language
        self.__language = new_language

    @last_login.setter
    def last_login(self, value: datetime) -> None:
        # Update user last_login
        print('value: ', value)
        self.__last_login = self.set_current_date()

    @name.setter
    def name(self, new_name: str) -> None:
        # Update user first_name
        self.__name = new_name

    @password_hash.setter
    def password_hash(self, password: str) -> None:
        # Generate password_hash
        print('new_password: ', password)
        self.generate_password(password)

    @picture.setter
    def picture(self, new_picture: object) -> None:
        # Update user picture
        print('uploading new picture')
        self.__picture = new_picture

    @profile.setter
    def profile(self, new_profile: str) -> None:
        # Update user profile
        self.__profile = new_profile

    @provider.setter
    def provider(self, new_provider: str) -> None:
        # Update user provider
        self.__provider = new_provider

    @session_token.setter
    def session_token(self, new_session_token: str) -> None:
        # Update user session_token
        print('new_session_token: ', new_session_token)
        self.__session_token = self.generate_token(600)

    @username.setter
    def username(self, new_username: str) -> None:
        # Update user last_name
        self.__username = new_username

    @user_groups.setter
    def user_groups(self, new_user_groups: list) -> None:
        # Update user_groups
        self.__user_groups = new_user_groups

    @user_groups_manager.setter
    def user_groups_manager(self, new_user_groups_manager: list) -> None:
        # Update user_groups_manager
        self.__user_groups_manager = new_user_groups_manager

    def set_user_group(self, new_group: str) -> bool:
        # Validate if new_group already exist is user_group
        if new_group not in self.__user_groups:
            # Add new group to user_group
            self.__user_groups.append(new_group)
            return True
        return False

    def set_user_groups_manager(self, new_group_manager) -> bool:
        # Validate if new_group_manager already exist in user_group_manager
        if new_group_manager not in self.__user_groups_manager:
            # Add new_group_manager to user_groups_manager
            self.__user_groups_manager.append(new_group_manager)
            return True
        return False

    # -------------- methods
    def is_active(self) -> bool:
        # User active status
        return self.__active

    def is_anonymous(self) -> bool:
        # User anonymous status
        return False

    def is_authenticated(self) -> bool:
        # User authenticated status
        print('is_authenticated: ', self.__authenticated)
        return self.__authenticated

    def generate_token(self, expiration=600) -> str:
        # Generate session_token
        s = Serializer(Config.SECRET_KEY,
                       expires_in=expiration)
        return s.dumps({'email': self.__email})

    def get_id(self):
        # Return user id
        print('self.__session_token: ', self.__session_token)
        print('type(self.__session_token): ', type(self.__session_token))
        return self.__session_token

    def validate_password(self, password: str) -> bool:
        # Validate current user password with a provided password
        password_validation = check_password_hash(self.password_hash, password)
        return password_validation

    # ----------------- static methods
    @staticmethod
    def generate_password(password) -> str:
        # Generate hash password
        return generate_password_hash(password=password,
                                      method='pbkdf2:sha256',
                                      salt_length=15)

    @staticmethod
    def set_current_date() -> datetime:
        # Current datetime
        return datetime.datetime.utcnow()

    @staticmethod
    def verify_token(token) -> object:
        # Validate a token
        s = Serializer(Config.SECRET_KEY)

        try:
            data = s.loads(token)
        except SignatureExpired:
            print('Valid token, but expired')
            return None   # Valid token, but expired
        except BadSignature:
            print('Invalid token')
            return None   # Invalid token
        # Retrieve user by email
        print('------------------ get_user_by_email')
        user = mongo.db.users.find_one({'email': data['email']})
        print('user: ', user)
        return user
