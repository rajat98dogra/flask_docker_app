from wtforms import SubmitField, StringField, PasswordField,\
    IntegerField, DateTimeField,DateField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, EqualTo, Email
from .model import User

def myvalidator(form,field):
    if len(str(field.data))>10:
        # print('\n\n\n', field.data)
        raise ValueError('length should be less than equal to 10')

class Details(FlaskForm):
    firstname = StringField('firstname', validators=[DataRequired(), Length(min=4, max=20)])
    lastname = StringField('lastname', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('email', validators=[DataRequired(), Email()])
    phone = IntegerField('phone', validators=[DataRequired(),myvalidator])
    address = StringField('address', validators=[DataRequired(), Length(min=0,max=100)])
    dob = DateField('dob', validators=[DataRequired()])

class Loginform(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired(), Length(min=4, max=10)])
    submit=SubmitField('Log In')

class RegisterationForm(Details):
    password = PasswordField('password', validators=[DataRequired(), Length(min=4, max=10)])
    confirmpassword = PasswordField('confirmpassword',
                                    validators=[ EqualTo('password')])
    submit = SubmitField('Submit')

class UserUpdateform(Details):
    submit=SubmitField('Update')

class AdminUpdateform(FlaskForm):
    firstname = StringField('firstname', validators=[DataRequired(), Length(min=4, max=20)])
    lastname = StringField('lastname', validators=[DataRequired(), Length(min=4, max=20)])
    roll=StringField('Roll')
    submit=SubmitField('Update')
