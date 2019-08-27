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
        self.__caseStatus = case['status']
        self.__caseType = case['type']
        self.__groups = case['groups'] if 'groups' in case else []
        
        self.__clientId = case['clientId']
        self.__clientName = case['clientName']
        
        self.__creationDate = self.set_current_date()
        self.__dueDate = self.string_to_datetime(case['dueDate'])
        self.__lastModificationDate = self.set_current_date()

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
                           self.__caseStatus,
                           self.__caseType,
                           self.__groups,
                           self.__clientId,
                           self.__clientName,
                           self.__creationDate,
                           self.__dueDate,
                           self.__lastModificationDate))

        # -------------- getters

    @property
    def serialize(self) -> dict:
        # Return object data in easily serializable format
        print('Case Model - Serialize...')
        return {
            'caseId': self.__id,
            'name': self.__name,
            'description': self.__description,
            'status': self.__caseStatus,
            'type': self.__caseType,
            'groups': self.__groups,
            'clientId': self.__clientId,
            'clientName': self.__clientName,
            'creationDate': self.__creationDate,
            'dueDate': self.__dueDate,
            'lastModification': self.__lastModificationDate,
        }

    # ---------------------------- properties
    @property
    def caseId(self) -> str:
        # Return caseId
        return self.__id

    @property
    def caseStatus(self) -> str:
        # Return caseStatus
        return self.__caseStatus

    @property
    def caseType(self) -> str:
        # Return case type
        return self.__caseType

    @property
    def clientId(self) -> str:
        # Return case clientId
        return self.__clientId

    @property
    def clientName(self) -> str:
        # Return case clientName
        return self.__clientName

    @property
    def creationDate(self) -> datetime:
        # Return case creation date
        return self.__creationDate

    @property
    def description(self) -> str:
        # Return case description
        return self.__description

    @property
    def dueDate(self) -> datetime:
        # Return case dueDate
        return self.__dueDate

    @property
    def groups(self) -> list:
        # Return case group
        return self.__groups

    @property
    def id(self) -> str:
        # Return case id
        return self.__id

    @property
    def lastModificationDate(self) -> datetime:
        # Return case last modification date
        return self.__lastModificationDate

    @property
    def name(self) -> str:
        # Return case name
        return self.__name

    # ---------------------------- setters
    @caseStatus.setter
    def caseStatus(self, new_status) -> None:
        # Set new_status
        self.caseStatus = new_status

    @caseType.setter
    def caseType(self, new_type) -> None:
        # Set new_type
        self.__caseType = new_type

    @clientId.setter
    def clientId(self, new_clientId) -> None:
        # Set new clientId
        self.__clientId = new_clientId

    @clientName.setter
    def clientName(self, new_clientName) -> None:
        # Set new clientName
        self.__clientName = new_clientName

    @creationDate.setter
    def creationDate(self, new_date) -> None:
        # Set new case creation date
        print('new_date: ', new_date)
        self.__creationDate = self.set_current_date()

    @description.setter
    def description(self, new_description) -> None:
        # Set new case description
        self.__description = new_description

    @dueDate.setter
    def dueDate(self, new_dueDate) -> None:
        # Set new dueDate
        self.__dueDate = new_dueDate

    @groups.setter
    def groups(self, new_group_name) -> None:
        # Set new_user
        self.__groups.append(new_group_name)

    @id.setter
    def id(self, new_id) -> None:
        # Set new case id
        self.__id = new_id

    @lastModificationDate.setter
    def lastModificationDate(self, new_date) -> None:
        # Set new case lastModificationDate
        print('new_date: ', new_date)
        self.__lastModificationDate = self.set_current_date()

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
        print('string_date: ', string_date)
        return datetime.strptime(string_date, '%Y-%m-%dT%H:%M:%S')
