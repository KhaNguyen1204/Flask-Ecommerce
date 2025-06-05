from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, FloatField, SelectField, DateField, HiddenField
from wtforms.validators import DataRequired, Length, NumberRange, Optional
from flask_wtf.file import FileField, FileAllowed

class WarehouseForm(FlaskForm):
    name = StringField('Tên kho', validators=[DataRequired(), Length(min=2, max=100)])
    location = StringField('Địa chỉ', validators=[DataRequired(), Length(min=2, max=255)])
    capacity = IntegerField('Sức chứa', validators=[Optional(), NumberRange(min=0)])
    description = TextAreaField('Mô tả', validators=[Optional()])
    manager_id = SelectField('Người quản lý', coerce=int, validators=[Optional()])
    status = SelectField('Trạng thái', choices=[
        ('active', 'Hoạt động'),
        ('inactive', 'Không hoạt động'),
    ], validators=[DataRequired()])

class InboundReceiptForm(FlaskForm):
    receipt_number = StringField('Số phiếu nhập', validators=[DataRequired(), Length(min=3, max=50)])
    receipt_date = DateField('Ngày nhập', format='%Y-%m-%d', validators=[DataRequired()])
    supplier = StringField('Nhà cung cấp', validators=[Optional(), Length(max=100)])
    warehouse_id = SelectField('Kho', coerce=int, validators=[DataRequired()])
    notes = TextAreaField('Ghi chú', validators=[Optional()])
    status = SelectField('Trạng thái', choices=[
        ('pending', 'Chờ xử lý'),
        ('completed', 'Hoàn thành'),
        ('cancelled', 'Đã hủy')
    ], default='pending')

class InboundReceiptDetailForm(FlaskForm):
    product_id = SelectField('Sản phẩm', coerce=int, validators=[DataRequired()])
    quantity = IntegerField('Số lượng', validators=[DataRequired(), NumberRange(min=1)])
    price = FloatField('Đơn giá', validators=[DataRequired(), NumberRange(min=0)])  # Thay đổi từ unit_price thành price
    notes = TextAreaField('Ghi chú', validators=[Optional()])

class OutboundReceiptForm(FlaskForm):
    receipt_number = StringField('Số phiếu xuất', validators=[DataRequired(), Length(min=3, max=50)])
    receipt_date = DateField('Ngày xuất', format='%Y-%m-%d', validators=[DataRequired()])
    recipient = StringField('Người nhận', validators=[Optional(), Length(max=100)])
    warehouse_id = SelectField('Kho', coerce=int, validators=[DataRequired()])
    notes = TextAreaField('Ghi chú', validators=[Optional()])
    status = SelectField('Trạng thái', choices=[
        ('pending', 'Chờ xử lý'),
        ('completed', 'Hoàn thành'),
        ('cancelled', 'Đã hủy')
    ], default='pending')

class OutboundReceiptDetailForm(FlaskForm):
    product_id = SelectField('Sản phẩm', coerce=int, validators=[DataRequired()])
    quantity = IntegerField('Số lượng', validators=[DataRequired(), NumberRange(min=1)])
    price = FloatField('Đơn giá', validators=[DataRequired(), NumberRange(min=0)])  # Thay đổi từ unit_price thành price
    notes = TextAreaField('Ghi chú', validators=[Optional()])

class SearchForm(FlaskForm):
    keyword = StringField('Từ khóa')
    status = SelectField('Trạng thái', choices=[
        ('', 'Tất cả'),
        ('active', 'Hoạt động'),
        ('inactive', 'Không hoạt động'),
        ('pending', 'Chờ xử lý'),
        ('completed', 'Hoàn thành'),
        ('cancelled', 'Đã hủy')
    ], validators=[Optional()])
    date_from = DateField('Từ ngày', format='%Y-%m-%d', validators=[Optional()])
    date_to = DateField('Đến ngày', format='%Y-%m-%d', validators=[Optional()])
