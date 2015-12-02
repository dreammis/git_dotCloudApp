# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField,TextAreaField,BooleanField,SelectField
from flask.ext.pagedown.fields import PageDownField
from wtforms.validators import Required,Length,Email,Regexp
from ..models import Role,User
from wtforms import ValidationError



class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')
class EditProfileForm(Form):
    name = StringField('Real name',validators=[Length(0,64)])
    location = StringField('Location',validators=[Length(0,64)])
    about_me = TextAreaField('About Me')
    submit = SubmitField('Submit')

class EditProfileAdminForm(Form):
    email = StringField('Email',validators=[Required(),Length(1,64),Email()])
    username = StringField('Username',validators=[
        Required(),Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,
                                       '用户名必须是英文、数字、点、或者下划线.')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role',coerce=int)
    name = StringField('Real name',validators=[Length(0,64)])
    location = StringField('Location',validators=[Length(0,64)])
    about_me = TextAreaField('About Me')
    submit = SubmitField('Submit')

    def __init__(self,user,*args,**kwargs):
        super(EditProfileAdminForm,self).__init__(*args,**kwargs)
        self.role.choices = [(role.id,role.name)for role in Role.query.order_by(Role.name).all()]
        self.user = user
    def validate_email(self,field):
        if field.data != self.user.email and \
            User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self,field):
        if field.data!= self.user.username and \
            User.query.filter_by(username = field.data).first():
            raise ValidationError('Username already in use.')
class PostForm(Form):
    body = PageDownField('What\'s on your mind?',validators=[Required()],
                         default='''##你可以使用MarkDown ohh!!!
>**注意：**这个马克党和我原来用的不太一样，至少代码块我是没搞出来额。
                         ''')
    submit = SubmitField('Submit')

class CommentForm(Form):
    body = StringField('Enter your comment', validators=[Required()])
    submit = SubmitField('Submit')