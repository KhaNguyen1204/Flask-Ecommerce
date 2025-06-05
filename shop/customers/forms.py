from wtforms import Form, StringField, TextAreaField, PasswordField, SubmitField, validators, ValidationError, IntegerField
from flask_wtf.file import FileRequired, FileAllowed, FileField
from flask_wtf import FlaskForm
from shop.models import User

class CustomerRegisterForm(FlaskForm):
    username= StringField('Username: ', [validators.DataRequired()])
    email = StringField('Email: ', validators=[validators.Email(), validators.DataRequired()])
    phone = StringField('Phone: ', [validators.DataRequired()])
    password = PasswordField('Password: ', validators=[validators.DataRequired(), validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Password: ')
    country = StringField('Country: ', [validators.DataRequired()])
    city = StringField('City: ', [validators.DataRequired()])
    address = TextAreaField('Address: ', [validators.DataRequired()])
    zipcode = StringField('Zipcode: ', [validators.DataRequired()])
    profile = FileField('Profile: ', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'], 'Images only!')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError('Username already exists! Please choose a different one.')

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('Email already exists! Please choose a different one.')

    def validate_phone(self, phone):
        if User.query.filter_by(phone=phone.data).first():
            raise ValidationError('Contact already exists! Please choose a different one.')

class ReviewForm(FlaskForm):
    rating = IntegerField('Rating (1-5)', [validators.DataRequired(), validators.NumberRange(min=1, max=5)])
    comment = TextAreaField('Comment', [validators.Optional(), validators.Length(max=1000)])
    submit = SubmitField('Submit Review')


