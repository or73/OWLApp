"""
File Path: application/modules/group/models.py
Description: Case models for App - Define Case models
Copyright (c) 2019. This Application has been developed by OR73.
"""
import datetime


class Group:
    def __init__(self, group):
        print('group: ', group)
        self.__id = group['_id']
        self.__name = group['name']
        self.__description = group['description']
        self.__creation_date = self.set_current_date()
        self.__last_modification_date = self.set_current_date()
        self.__managers = group['user_groups_manager']
        self.__users = group['user_groups']

    def __repr__(self) -> str:
        return '<Group\n name: {}\nDescription: {}\nCreation Date: {}\nLast Modification: {}\nmanagers: {}\nUsers: {}' \
            .format(self.__name, self.__description, self.__creation_date, self.__last_modification_date,
                    self.__managers, self.__users)

    # -------------- getters
    @property
    def serialize(self) -> dict:
        # Return object data in easily serializable format
        return {
            'name': self.__name,
            'description': self.__description,
            'creation_date': self.__creation_date,
            'last_modification': self.__last_modification_date,
            'managers': self.__managers,
            'users': self.__users
        }

    @property
    def id(self) -> str:
        # Return group id
        return self.__id

    @property
    def name(self) -> str:
        # Return group name
        return self.__name

    @property
    def description(self) -> str:
        # Return group description
        return self.__description

    @property
    def creation_date(self) -> datetime:
        # Return group creation date
        return self.__creation_date

    @property
    def last_modification_date(self) -> datetime:
        # Return last_modification_date
        return self.__last_modification_date

    @property
    def managers(self) -> list:
        # Return managers list
        return self.__managers

    @property
    def users(self) -> list:
        # Return users list
        return self.__users

    # -------------- setters
    @id.setter
    def id(self, new_id: str) -> None:
        # Set id
        self.__id = new_id

    @name.setter
    def name(self, new_name: str) -> None:
        # Set name
        self.__name = new_name

    @description.setter
    def description(self, new_description: str) -> None:
        # Set description
        self.__description = new_description

    @creation_date.setter
    def creation_date(self, new_creation_date: datetime) -> None:
        print('new_creation_date: ', new_creation_date)
        # Set creation_date
        self.__creation_date = self.set_current_date()

    @last_modification_date.setter
    def last_modification_date(self, new_last_modification_date):
        # Set last_modification_date
        print('new_last_modification_date: ', new_last_modification_date)
        self.__last_modification_date = self.set_current_date()

    @managers.setter
    def managers(self, new_managers_list: list) -> None:
        # Set managers list
        self.__managers = new_managers_list

    @users.setter
    def users(self, new_users_list: list) -> None:
        # Set users list
        self.__users = new_users_list

    def set_manager(self, new_manager: str) -> bool:
        # Validate if new_manager does not already exist in managers list
        if new_manager not in self.__managers:
            # Add a manager to manager list
            self.__managers.append(new_manager)
            return True
        return False

    def set_user(self, new_user: str) -> bool:
        # Validate if new_user does not already exist in users list
        if new_user not in self.__users:
            # Add a user to users list
            self.__users.append(new_user)
            return True
        return False

    # -------------- static methods
    @staticmethod
    def set_current_date():
        # Set current date
        return datetime.datetime.utcnow()
