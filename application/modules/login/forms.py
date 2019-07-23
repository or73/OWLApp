"""
File Path: application/modules/login/forms.py
Description: Login forms for App - Define login forms
Copyright (c) 2019. This Application has been developed by OR73.
"""
from wtforms import BooleanField, Form, PasswordField, StringField, validators
from wtforms.validators import DataRequired, Email, InputRequired


class ValidateLoginForm(Form):
    """ Validate login form fields """
    print('----------------- ValidateLoginForm')
    email = StringField('Email',
                        validators=[DataRequired(message='Enter a valid email or username'),
                                    InputRequired(message='Enter a valid email or username')])
    password = PasswordField('Password',
                             validators=[DataRequired(message='Enter a password min 3 length'),
                                         InputRequired(message='Enter a password min 3 length'),
                                         validators.Length(min=3, max=35)])
    remember = BooleanField('Remember')
