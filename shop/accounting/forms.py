import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, DateField, validators

class RevenueReportForm(FlaskForm):
    start_date = DateField('Ngày bắt đầu', format='%Y-%m-%d', validators=[validators.DataRequired()],
                           default=datetime.date.today() - datetime.timedelta(days=30))
    end_date = DateField('Ngày kết thúc', format='%Y-%m-%d', validators=[validators.DataRequired()],
                            default=datetime.date.today())
    report_type = SelectField('Loại báo cáo'
                              , choices=[
                                ('sumary', 'Tổng hợp'),
                                ('daily', 'Báo cáo theo ngày'),
                                ('monthly', 'Báo cáo theo tháng'),
                                ('yearly', 'Báo cáo theo năm')])
    
    submit = SubmitField('Tạo báo cáo')
