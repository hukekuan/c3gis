#-*- coding:utf-8 -*-
#!/usr/bin/env python
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired,Length, Email

class LoginForm(FlaskForm):
    username = StringField('UserName',validators=[DataRequired(),Length(2,25)])
    password = PasswordField('PassWord',validators=[DataRequired(),Length(2,25)])