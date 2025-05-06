from wtforms import Form, StringField, TextAreaField, PasswordField, SubmitField, validators, ValidationError
from flask_wtf.file import FileRequired, FileAllowed, FileField
from flask_wtf import FlaskForm
from .model import Register

class CustomerRegisterForm(FlaskForm):
    __tablename__ = 'customers'
    name = StringField('Name: ')
    username= StringField('Username: ', [validators.DataRequired()])
    email = StringField('Email: ', validators=[validators.Email(), validators.DataRequired()])
    password = PasswordField('Password: ', validators=[validators.DataRequired(), validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Password: ')
    country = StringField('Country: ', [validators.DataRequired()])
    city = StringField('City: ', [validators.DataRequired()])
    contact = StringField('Contact: ', [validators.DataRequired()])
    address = TextAreaField('Address: ', [validators.DataRequired()])
    zipcode = StringField('Zipcode: ', [validators.DataRequired()])

    profile = FileField('Profile: ', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'], 'Images only!')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        if Register.query.filter_by(username=username.data).first():
            raise ValidationError('Username already exists! Please choose a different one.')

    def validate_email(self, email):
        if Register.query.filter_by(email=email.data).first():
            raise ValidationError('Email already exists! Please choose a different one.')

    def validate_number(self, contact):
        if Register.query.filter_by(contact=contact.data).first():
            raise ValidationError('Contact already exists! Please choose a different one.')

class CustomerLoginForm(FlaskForm):
    email = StringField('Email: ', validators=[validators.Email(), validators.DataRequired()])
    password = PasswordField('Password: ', validators=[validators.DataRequired()])

    #submit = SubmitField('Login')




