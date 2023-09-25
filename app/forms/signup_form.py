from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Email, ValidationError
from email_validator import validate_email, EmailNotValidError
from app.models import User


def email_is_valid(form, field):
    # Checking if email is valid
    email = field.data
    # print(email, "***********************EMAIL***********************")
    try:
        emailinfo = validate_email(email, check_deliverability=False)
        print(emailinfo, "*****EMAILINFO******")
        emailinfo = emailinfo.normalized
    except EmailNotValidError as e:
        print(str(e))
        raise ValidationError('Please use valid email address.')

def user_exists(form, field):
    # Checking if user exists
    email = field.data
    user = User.query.filter(User.email == email).first()
    # print(user, "***********************USER***********************")
    if user:
        raise ValidationError('Email address is already in use.')

def username_exists(form, field):
    # Checking if username is already in use
    username = field.data
    user = User.query.filter(User.username == username).first()
    if user:
        raise ValidationError('Username is already in use.')

def phone_exists(form, field):
    # Checking if phone is already in use
    phone = field.data
    user = User.query.filter(User.phone == phone).first()
    if user:
        raise ValidationError('Phonenumber is already in use.')

def phone_is_number(form, field):
    # Checking if phone is number
    if int(field.data):
        phone = field.data
    else:
        raise ValidationError('Phonenumber must be a 10 digit number.')


class SignUpForm(FlaskForm):
    username = StringField(
        'username', validators=[DataRequired(), username_exists])
    firstName = StringField('firstName', validators=[DataRequired()])
    lastName = StringField('lastName', validators=[DataRequired()])
    phone = StringField('phone', validators=[DataRequired(), phone_exists, phone_is_number])
    location = StringField('location', validators=[DataRequired()])
    isTasker = BooleanField('isTasker')
    email = StringField('email', validators=[DataRequired(), user_exists, email_is_valid])
    password = StringField('password', validators=[DataRequired()])
