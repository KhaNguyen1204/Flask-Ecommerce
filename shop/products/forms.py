from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import Form, IntegerField, StringField, BooleanField, TextAreaField, validators, DecimalField

class AddProducts(Form):
    name = StringField('Tên sản phẩm', [validators.DataRequired()])
    price = DecimalField('Giá', [validators.DataRequired()])
    discount = IntegerField('Khuyến mãi', default=0)
    stock = IntegerField('Số lượng', [validators.DataRequired()])
    description = TextAreaField('Mô tả', [validators.DataRequired()])
    colors = TextAreaField('Màu sắc', [validators.DataRequired()])
    image_1 = FileField('Hình ảnh 1', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'], 'Yêu cầu hình ảnh!')])
    image_2 = FileField('Hình ảnh 2', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'], 'Yêu cầu hình ảnh!')])
    image_3 = FileField('Hình ảnh 3', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'], 'Yêu cầu hình ảnh!')])
    #is_available = BooleanField('Is Available')

