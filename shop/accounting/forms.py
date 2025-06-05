import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, DateField, validators

class RevenueReportForm(FlaskForm):
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[validators.DataRequired()],
                           default=datetime.date.today() - datetime.timedelta(days=30))
    end_date = DateField('End Date', format='%Y-%m-%d', validators=[validators.DataRequired()],
                            default=datetime.date.today())
    report_type = SelectField('Report Type'
                              , choices=[
                                ('sumary', 'Summary'),
                                ('daily', 'Daily Breakdown'),
                                ('monthly', 'Monthly Breakdown'),
                                ('yearly', 'Yearly Breakdown')])
    
    submit = SubmitField('Generate Report')
