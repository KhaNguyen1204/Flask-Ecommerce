from wtforms import Form, StringField, TextAreaField, PasswordField, SubmitField, validators, ValidationError, IntegerField
from flask_wtf.file import FileRequired, FileAllowed, FileField
from flask_wtf import FlaskForm
from shop.models import User

class CustomerRegisterForm(FlaskForm):
    username= StringField('Tên người dùng', [validators.DataRequired()])
    email = StringField('Email', validators=[validators.Email(), validators.DataRequired()])
    phone = StringField('Số điện thoại', [validators.DataRequired()])
    password = PasswordField('Mật khẩu', validators=[validators.DataRequired(), validators.EqualTo('confirm', message='Mật khẩu phải trùng khớp')])
    confirm = PasswordField('Xác nhận mật khẩu')
    country = StringField('Quốc gia', [validators.DataRequired()])
    city = StringField('Thành phố', [validators.DataRequired()])
    address = TextAreaField('Địa chỉ', [validators.DataRequired()])
    profile = FileField('Ảnh đại diện', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'], 'Chỉ nhận hình ảnh!')])
    submit = SubmitField('Đăng ký')

    # def validate_username(self, username):
    #     if User.query.filter_by(username=username.data).first():
    #         raise ValidationError('Tên người dùng đã tồn tại, hãy chọn một tên khác.')
    #
    # def validate_email(self, email):
    #     if User.query.filter_by(email=email.data).first():
    #         raise ValidationError('Email đã tồn tại, vui lòng chọn 1 email khác.')
    #
    # def validate_phone(self, phone):
    #     if User.query.filter_by(phone=phone.data).first():
    #         raise ValidationError('Số điện thoại đã tồn tại, vui lòng chọn 1 số điện thoại khác.')

class ReviewForm(FlaskForm):
    rating = IntegerField('Đánh giá từ 1 --> 5', [validators.DataRequired(), validators.NumberRange(min=1, max=5)])
    comment = TextAreaField('Nhận xét', [validators.Optional(), validators.Length(max=1000)])
    submit = SubmitField('Đăng nhận xét')


