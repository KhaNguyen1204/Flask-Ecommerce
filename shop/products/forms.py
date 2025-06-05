from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import Form, IntegerField, StringField, BooleanField, TextAreaField, validators, DecimalField

class AddProducts(Form):
    name = StringField('Name', [validators.DataRequired()])
    price = DecimalField('Price', [validators.DataRequired()])
    discount = IntegerField('Discount', default=0)
    stock = IntegerField('Stock', [validators.DataRequired()])
    description = TextAreaField('Description', [validators.DataRequired()])
    colors = TextAreaField('Colors', [validators.DataRequired()])
    image_1 = FileField('Image_1', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'], 'Images only!')])
    image_2 = FileField('Image_2', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'], 'Images only!')])
    image_3 = FileField('Image_3', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'], 'Images only!')])
    #is_available = BooleanField('Is Available')

