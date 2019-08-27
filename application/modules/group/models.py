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
        self.__creationDate = self.set_current_date()
        self.__lastModificationDate = self.set_current_date()
        self.__managers = group['user_groups_manager']
        self.__users = group['user_groups']

    def __repr__(self) -> str:
        return '<Group\n name: {}\nDescription: {}\nCreation Date: {}\nLast Modification: {}\nmanagers: {}\nUsers: {}' \
            .format(self.__name, self.__description, self.__creationDate, self.__lastModificationDate,
                    self.__managers, self.__users)

    # -------------- getters
    @property
    def serialize(self) -> dict:
        # Return object data in easily serializable format
        return {
            'name': self.__name,
            'description': self.__description,
            'creationDate': self.__creationDate,
            'lastModification': self.__lastModificationDate,
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
    def creationDate(self) -> datetime:
        # Return group creation date
        return self.__creationDate

    @property
    def lastModificationDate(self) -> datetime:
        # Return lastModificationDate
        return self.__lastModificationDate

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

    @creationDate.setter
    def creationDate(self, new_creationDate: datetime) -> None:
        print('new_creationDate: ', new_creationDate)
        # Set creationDate
        self.__creationDate = self.set_current_date()

    @lastModificationDate.setter
    def lastModificationDate(self, new_lastModificationDate):
        # Set lastModificationDate
        print('new_lastModificationDate: ', new_lastModificationDate)
        self.__lastModificationDate = self.set_current_date()

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
