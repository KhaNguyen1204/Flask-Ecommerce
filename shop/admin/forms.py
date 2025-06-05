from wtforms import Form, StringField, PasswordField, validators, SubmitField
from flask_wtf import FlaskForm
from wtforms.fields.choices import SelectField
from shop.models import User, Role


class StaffRegistrationForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35), validators.Email()])
    phone = StringField('Phone Number', [validators.DataRequired(), validators.Length(min=5, max=15)])
    password = PasswordField('New Password', [
        validators.DataRequired(), validators.Length(min=6, max=30),
        validators.EqualTo('confirm', message='Passwords must match')])
    position = StringField('Position', [validators.DataRequired()])
    role_id = SelectField('Role', coerce=int)
    confirm = PasswordField('Repeat Password')
    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        super(StaffRegistrationForm, self).__init__(*args, **kwargs)
        # Populate role choices with your specific roles
        self.role_id.choices = [(role.id, role.name)
                                for role in Role.query.filter(Role.name.in_(
                ['admin', 'sales', 'accounting', 'warehouse']
            )).all()]


class LoginForm(Form):
    email = StringField('Email Address', [validators.Length(min=6, max=35), validators.Email()])
    password = PasswordField('Password', [validators.DataRequired()])


class RoleForm(FlaskForm):
    name = StringField('Role Name', [validators.DataRequired()])
    description = StringField('Description', [validators.DataRequired()])
    submit = SubmitField()


class ChangePasswordForm(Form):
    old_password = PasswordField('Current Password', [validators.DataRequired()])
    new_password = PasswordField('New Password',
                                 validators=[validators.DataRequired(), validators.Length(min=6, max=30)])
    confirm = PasswordField('Repeat Password', validators=[validators.DataRequired(), validators.EqualTo('new_password',
                                                                                                         message='Passwords must match')])
