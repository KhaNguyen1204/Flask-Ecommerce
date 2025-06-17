from wtforms import Form, StringField, PasswordField, validators, SubmitField
from flask_wtf import FlaskForm
from wtforms.fields.choices import SelectField
from shop.models import User, Role


class StaffRegistrationForm(FlaskForm):
    username = StringField('Tên nhân viên', [validators.Length(min=4, max=30, message='Tên nhân viên phải từ 4 đến 30 ký tự')])
    email = StringField('Email', [validators.Length(min=6, max=35, message="Email độ dài từ 6 đến 35 ký tự"), validators.Email()])
    phone = StringField('Số điện thoại', [validators.DataRequired(), validators.Length(min=10, max=11, message='Số điện thoại phải từ 10 đến 11 ký tự')])
    password = PasswordField('Mật khẩu', [
        validators.DataRequired(), validators.Length(min=6, max=30, message='Mật khẩu phải từ 6 đến 30 ký tự'),
        validators.EqualTo('confirm', message='Mật khẩu phải trùng khớp')])
    position = StringField('Ví trí', [validators.DataRequired()])
    role_id = SelectField('Vai trò trong trang web', coerce=int)
    confirm = PasswordField('Xác nhân mật khẩu')
    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        super(StaffRegistrationForm, self).__init__(*args, **kwargs)
        # Populate role choices with your specific roles
        self.role_id.choices = [(role.id, role.name)
                                for role in Role.query.filter(Role.name.in_(
                ['admin', 'sales', 'accounting', 'warehouse']
            )).all()]


class LoginForm(Form):
    email = StringField('Email', [validators.Length(min=6, max=30), validators.Email()])
    password = PasswordField('Mật khẩu', [validators.DataRequired()])


class RoleForm(FlaskForm):
    name = StringField('Tên vai trò', [validators.DataRequired()])
    description = StringField('Mô tả', [validators.DataRequired()])
    submit = SubmitField()


class ChangePasswordForm(Form):
    old_password = PasswordField('Mật khẩu hiện tại', [validators.DataRequired()])
    new_password = PasswordField('Mật khẩu mới',
                                 validators=[validators.DataRequired(), validators.Length(min=6, max=30)])
    confirm = PasswordField('Xác nhận mật khẩu', validators=[validators.DataRequired(), validators.EqualTo('new_password',
                                                                                                         message='Mật khẩu phải trùng khớp')])
