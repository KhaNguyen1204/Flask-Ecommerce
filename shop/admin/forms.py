from wtforms import Form, StringField, PasswordField, validators, SubmitField
from flask_wtf import FlaskForm
from wtforms.fields.choices import SelectField
from shop.models import User, Role


class StaffRegistrationForm(FlaskForm):
    username = StringField('Tên nhân viên', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=35), validators.Email()])
    phone = StringField('Số điện thoại', [validators.DataRequired(), validators.Length(min=5, max=15)])
    password = PasswordField('Mật khẩu', [
        validators.DataRequired(), validators.Length(min=6, max=30),
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
    email = StringField('Email', [validators.Length(min=6, max=35), validators.Email()])
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
