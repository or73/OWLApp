"""
File Path: application/modules/case/models.py
Description: Case models for App - Define Case models
Copyright (c) 2019. This Application has been developed by OR73.
"""
from datetime import datetime


class Case:
    def __init__(self, case):
        self.__id = case['id']
        self.__name = case['name']
        self.__description = case['description']
        self.__case_status = case['status']
        self.__case_type = case['type']

        self.__client_id = case['client_id']
        self.__client_name = case['client_name']
        self.__groups = case['groups'] if 'groups' in case else []

        self.__creation_date = self.set_current_date()
        self.__due_date = self.string_to_datetime(case['due_date'])
        self.__last_modification_date = self.set_current_date()

    def __repr__(self) -> str:
        return ('<\n'
                '\t-------   CASE DATA -------\n'
                '\tCase ID: {}\n'
                '\tCase name: {}\n'
                '\tDescription: {}\n'
                '\tCase Status: {}\n'
                '\tCase Type: {}\n'
                '\t-------   CASE ADDITIONAL DATA -------\n'
                '\tCase Groups: {}\n'
                '\tClient ID: {}\n'
                '\tClient name: {}\n'
                '\t-------   CASE DATES -------\n'
                '\tCreation Date: {}\n'
                '\tDue Date: {}\n'
                '\tLast Modification: {}\n'
                '>'.format(self.__id,
                           self.__name,
                           self.__description,
                           self.__case_status,
                           self.__case_type,
                           self.__groups,
                           self.__client_id,
                           self.__client_name,
                           self.__creation_date,
                           self.__due_date,
                           self.__last_modification_date))

        # -------------- getters

    @property
    def serialize(self) -> dict:
        # Return object data in easily serializable format
        print('Case Model - Serialize...')
        return {
            'case_id': self.__id,
            'name': self.__name,
            'description': self.__description,
            'status': self.__case_status,
            'type': self.__case_type,
            'groups': self.__groups,
            'client_id': self.__client_id,
            'client_name': self.__client_name,
            'creation_date': self.__creation_date,
            'due_date': self.__due_date,
            'last_modification': self.__last_modification_date,
        }

    # ---------------------------- properties
    @property
    def case_id(self) -> str:
        # Return case_id
        return self.__id

    @property
    def case_status(self) -> str:
        # Return case_status
        return self.__case_status

    @property
    def case_type(self) -> str:
        # Return case type
        return self.__case_type

    @property
    def client_id(self) -> str:
        # Return case client_id
        return self.__client_id

    @property
    def client_name(self) -> str:
        # Return case client_name
        return self.__client_name

    @property
    def creation_date(self) -> datetime:
        # Return case creation date
        return self.__creation_date

    @property
    def description(self) -> str:
        # Return case description
        return self.__description

    @property
    def due_date(self) -> datetime:
        # Return case due_date
        return self.__due_date

    @property
    def groups(self) -> list:
        # Return case group
        return self.__groups

    @property
    def id(self) -> str:
        # Return case id
        return self.__id

    @property
    def last_modification_date(self) -> datetime:
        # Return case last modification date
        return self.__last_modification_date

    @property
    def name(self) -> str:
        # Return case name
        return self.__name

    # ---------------------------- setters
    @case_status.setter
    def case_status(self, new_status) -> None:
        # Set new_status
        self.case_status = new_status

    @case_type.setter
    def case_type(self, new_type) -> None:
        # Set new_type
        self.__case_type = new_type

    @client_id.setter
    def client_id(self, new_client_id) -> None:
        # Set new client_id
        self.__client_id = new_client_id

    @client_name.setter
    def client_name(self, new_client_name) -> None:
        # Set new client_name
        self.__client_name = new_client_name

    @creation_date.setter
    def creation_date(self, new_date) -> None:
        # Set new case creation date
        print('new_date: ', new_date)
        self.__creation_date = self.set_current_date()

    @description.setter
    def description(self, new_description) -> None:
        # Set new case description
        self.__description = new_description

    @due_date.setter
    def due_date(self, new_due_date) -> None:
        # Set new due_date
        self.__due_date = new_due_date

    @groups.setter
    def groups(self, new_group_name) -> None:
        # Set new_user
        self.__groups.append(new_group_name)

    @id.setter
    def id(self, new_id) -> None:
        # Set new case id
        self.__id = new_id

    @last_modification_date.setter
    def last_modification_date(self, new_date) -> None:
        # Set new case last_modification_date
        print('new_date: ', new_date)
        self.__last_modification_date = self.set_current_date()

    @name.setter
    def name(self, new_name) -> None:
        # Set new case name
        self.__name = new_name

    # ---------------------------- static methods
    @staticmethod
    def set_current_date() -> datetime:
        # Current datetime
        return datetime.utcnow()

    @staticmethod
    def string_to_datetime(string_date) -> datetime:
        # Convert string to datetime
        return datetime.strptime(string_date, '%Y-%m-%dT%H:%M:%S')
