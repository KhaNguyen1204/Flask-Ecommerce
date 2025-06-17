from flask_wtf.file import FileAllowed, FileField, FileRequired
from pyexpat.errors import messages
from wtforms import Form, IntegerField, StringField, BooleanField, TextAreaField, validators, DecimalField

class AddProducts(Form):
    name = StringField('Tên sản phẩm', [validators.DataRequired(), validators.Length(min=2, max=80, message='Tên sản phẩm phải từ 2 đến 80 ký tự')])
    price = DecimalField('Giá', [validators.DataRequired(), validators.NumberRange(min=0, message='Giá phải lớn hơn hoặc bằng 0')], places=2)
    discount = IntegerField('Khuyến mãi (%)', [validators.NumberRange(min=0, max=100, message='Khuyến mãi phải từ 0 đến 100%')] ,default=0)
    stock = IntegerField('Số lượng', [validators.DataRequired(), validators.NumberRange(min=0, message='Số lượng phải lớn hơn hoặc bằng 0')])
    description = TextAreaField('Mô tả sản phẩm', [validators.DataRequired()])
    colors = TextAreaField('Màu sắc (phân cách bởi dấu phẩy)', [validators.DataRequired()])
    image_1 = FileField('Ảnh chính', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg', 'webp'], 'Yêu cầu hình ảnh!')])
    image_2 = FileField('Ảnh phụ 1', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg', 'webp'], 'Yêu cầu hình ảnh!')])
    image_3 = FileField('Ảnh phụ 2', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg', 'webp'], 'Yêu cầu hình ảnh!')])
    #is_available = BooleanField('Is Available')

