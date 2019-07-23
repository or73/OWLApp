"""
File Path: application/modules/case/models.py
Description: Case models for App - Define Case models
Copyright (c) 2019. This Application has been developed by OR73.
"""
import datetime


class Case:
    def __init__(self, case):
        self.__id = case['_id']
        self.__name = case['name']
        self.__description = case['description']
        self.__creation_date = self.set_current_date()
        self.__last_modification_date = self.set_current_date()
        self.__groups = case['groups'] if len(case) > 0 else []

    def __repr__(self) -> str:
        return '<Case\n name: {}\nDescription: {}\nCreation Date: {}\nLast Modification: {}\nGroups: {}\n'\
            .format(self.__name, self.__description, self.__creation_date, self.__last_modification_date, self.__groups)

    # -------------- getters
    @property
    def serialize(self) -> dict:
        # Return object data in easily serializable format
        return {
            'name': self.__name,
            'description': self.__description,
            'creation_date': self.__creation_date,
            'last_modification': self.__last_modification_date,
            'groups': self.__groups
        }

    # ---------------------------- properties
    @property
    def id(self) -> str:
        # Return case id
        return self.__id

    @property
    def name(self) -> str:
        # Return case name
        return self.__name

    @property
    def description(self) -> str:
        # Return case description
        return self.__description

    @property
    def creation_date(self) -> datetime:
        # Return case creation date
        return self.__creation_date

    @property
    def last_modification_date(self) -> datetime:
        # Return case last modification date
        return self.__last_modification_date

    @property
    def groups(self) -> list:
        # Return case group
        return self.__groups

    # ---------------------------- setters
    @id.setter
    def id(self, new_id) -> None:
        # Set new case id
        self.__id = new_id

    @name.setter
    def name(self, new_name) -> None:
        # Set new case name
        self.__name = new_name

    @description.setter
    def description(self, new_description) -> None:
        # Set new case description
        self.__description = new_description

    @creation_date.setter
    def creation_date(self, new_date) -> None:
        # Set new case creation date
        print('new_date: ', new_date)
        self.__creation_date = self.set_current_date()

    @last_modification_date.setter
    def last_modification_date(self, new_date) -> None:
        # Set new case last_modification_date
        print('new_date: ', new_date)
        self.__last_modification_date = self.set_current_date()

    @groups.setter
    def groups(self, new_group_name) -> None:
        # Set new_user
        self.groups.append(new_group_name)

    # ---------------------------- static methods
    @staticmethod
    def set_current_date() -> datetime:
        # Current datetime
        return datetime.datetime.utcnow()
