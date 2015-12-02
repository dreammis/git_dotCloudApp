# -*- coding: utf-8 -*-
from flask .ext.wtf import Form
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import Required,Length,Email,Regexp,EqualTo
from wtforms import ValidationError
from ..models import User

class LoginForm(Form):
    email = StringField('Email',validators=[Required(),Length(1,64),Email()])
    password = PasswordField('Password',validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit =SubmitField('Log In')


class RegistrationForm(Form):
    email = StringField('Email',validators=[Required(),Length(1,64),Email()])
    username = StringField('Username',validators=[
        Required(),Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,
                                       '用户名必须是英文、数字、点、或者下划线.')])
    password = PasswordField('Password',validators=[
        Required(),EqualTo('password2',message='两次密码必须一致.')])
    password2 = PasswordField('Confirm Password',validators=[Required()])
    submit = SubmitField('Register')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已经被注册.')
    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户已经被注册.')

class ChangePasswordForm(Form):
    old_password = StringField('Old password',validators=[Required()])
    password = StringField('New password',validators=[
        Required(),EqualTo('password2',message='两次密码必须一致.')])
    password2 = PasswordField('Confirm Password',validators=[Required()])
    submit = SubmitField('Update Password')


class PasswordResetRequestForm(Form):
    email = StringField('Email',validators=[Required(),Length(1,64),Email()])
    submit= SubmitField('Reset Password.')

class PasswordResetForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                   Email()])
    password = PasswordField('New Password', validators=[
        Required(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField('Reset Password')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('Unknown email address.')

