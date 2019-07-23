"""
File path: application/modules/login/models.py
Description: Auth models for App - Define login data models
Copyright (c) 2019. This Application has been developed by OR73.
"""
import datetime


class Login:
    def __init__(self, user_id):
        # User session init fields
        print('__init__ - Login: user_id: ', user_id)
        self.__user_id = user_id
        self.__login_time = self.set_time()
        self.__logout_time = None

    def __repr__(self) -> str:
        return '<user_id: {}\nlogin_time: {}\nlogout_time: {}>'\
            .format(self.__user_id, self.__login_time, self.__logout_time)

    @property
    def serialize(self) -> object:
        # Return an object data in easily serializable format
        return {
            'user_id': self.__user_id,
            'login_time': self.__login_time,
            'logout_time': self.__logout_time
        }

    # ------------------ getters
    @property
    def user_id(self) -> str:
        # Return user_id
        return self.__user_id

    @property
    def login_time(self) -> datetime:
        # Return login_time
        return self.__login_time

    @property
    def logout_time(self) -> datetime:
        # Return logout_time
        return self.__logout_time

    # ------------------ setters
    @user_id.setter
    def user_id(self, user_id) -> None:
        # Update user_id
        self.__user_id = user_id

    @login_time.setter
    def login_time(self, value) -> None:
        # Update login_time
        print('value: ', value)
        self.__login_time = self.set_time()

    @logout_time.setter
    def logout_time(self, value) -> None:
        # Update logout_time
        print('value: ', value)
        self.__logout_time = self.set_time()

    # ------------------- static methods
    @staticmethod
    def set_time() -> datetime:
        # Return current datetime
        return datetime.datetime.utcnow()
