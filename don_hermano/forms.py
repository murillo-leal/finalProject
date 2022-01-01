#forms.py
from flask.app import Flask
from flask_uploads import IMAGES, UploadSet
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import IntegerField, PasswordField, StringField, TextAreaField, SubmitField
from wtforms.validators import (DataRequired, Email, Length, ValidationError,
                                equal_to, regexp)
from . import models

images = UploadSet('images', IMAGES)

def email_exists(form, field):
    if models.User.select().where(models.User.email == field.data).exists():
        raise ValidationError('User with email already exists')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class RegistrationForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    cellphone = StringField('Cellphone', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=6), equal_to('pass_confirm', message='Passwords must match')])
    pass_confirm = PasswordField('Confirm Password', validators=[DataRequired()])

    def check_email(self, field):
        if models.User.get(email=field.data):
            raise ValidationError('Your email has been registered already!')
            
    def check_username(self, field):
        if models.User.get(username=field.data):
            raise ValidationError('Your username has been registered already!')


class UpdateUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    cellphone = StringField('Cellphone', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])

    def check_email(self, field):
        if models.User.get(email=field.data):
            raise ValidationError('Your email has been registered already!')
            
    def check_username(self, field):
        if models.User.get(username=field.data):
            raise ValidationError('Your username has been registered already!')

class NewProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])            
    image = FileField('Product Image', validators=[FileRequired(), FileAllowed(images, 'Images only!')])
    size = StringField('Size', validators=[DataRequired()])
    count = IntegerField('Product Count', validators=[DataRequired()])
    value = IntegerField('Procut Value', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    details = StringField('Details', validators=[DataRequired()])
    
class EditProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])            
    image = FileField('Product Image', validators=[FileAllowed(images, 'Images only!')])
    size = StringField('Size') 
    count = IntegerField('Product Count', validators=[DataRequired()])
    value = IntegerField('Procut Value')
    category = StringField('Category')
    details = StringField('Details')