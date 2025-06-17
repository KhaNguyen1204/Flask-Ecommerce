from wtforms import Form, StringField, TextAreaField, PasswordField, SubmitField, validators, ValidationError, IntegerField
from flask_wtf.file import FileRequired, FileAllowed, FileField
from flask_wtf import FlaskForm
from shop.models import User

class CustomerRegisterForm(FlaskForm):
    username= StringField('Tên người dùng', [validators.DataRequired(), validators.Length(min=4, max=30, message='Tên người dùng phải từ 4 đến 30 ký tự')])
    email = StringField('Email', validators=[validators.Email(), validators.DataRequired(), validators.Length(min=6, max=35, message="Email độ dài từ 6 đến 35 ký tự")])
    phone = StringField('Số điện thoại', [validators.DataRequired(), validators.Length(min=10, max=11, message='Số điện thoại phải từ 10 đến 11 ký tự')])
    password = PasswordField('Mật khẩu', validators=[validators.DataRequired(), validators.EqualTo('confirm', message='Mật khẩu phải trùng khớp'), validators.Length(min=6, max=30, message='Mật khẩu phải từ 6 đến 30 ký tự')])
    confirm = PasswordField('Xác nhận mật khẩu')
    country = StringField('Quốc gia', [validators.DataRequired()])
    city = StringField('Thành phố', [validators.DataRequired()])
    address = TextAreaField('Địa chỉ', [validators.DataRequired()])
    profile = FileField('Ảnh đại diện', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'], 'Chỉ nhận hình ảnh!')])
    submit = SubmitField('Đăng ký')

class ReviewForm(FlaskForm):
    rating = IntegerField('Đánh giá từ 1 --> 5', [validators.DataRequired(), validators.NumberRange(min=1, max=5)])
    comment = TextAreaField('Nhận xét', [validators.Optional(), validators.Length(max=1000)])
    submit = SubmitField('Đăng nhận xét')


