from website import db, login_manager
from datetime import datetime
import json
from website.models import User
from website.admin.models import Staff


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))


class Customer(User):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    country = db.Column(db.String(50), unique=False)
    city = db.Column(db.String(50), unique=False)
    address = db.Column(db.String(200), unique=False)
    zipcode = db.Column(db.String(50), unique=False, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'customer',
    }


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    invoice = db.Column(db.String(100), unique=True, nullable=False)
    status = db.Column(db.String(100), unique=False, nullable=False, default='Pending')
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=True)

    # Các thông tin tổng hợp của đơn hàng
    subtotal = db.Column(db.Float, default=0.0)
    tax = db.Column(db.Float, default=0.0)
    grand_total = db.Column(db.Float, default=0.0)

    # Relationships
    customer = db.relationship('Customer', backref='orders', lazy=True)
    order_details = db.relationship('OrderDetail', backref='orders', lazy=True, cascade="all, delete-orphan")
    staff = db.relationship('Staff', backref='handled_orders', foreign_keys=[staff_id])

    def __repr__(self):
        return f'<Order {self.invoice}>'


class OrderDetail(db.Model):
    __tablename__ = 'order_details'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)

    # Thông tin sản phẩm
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    product_name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    discount = db.Column(db.Float, default=0.0)  # Lưu dưới dạng phần trăm

    # Các trường tính toán
    subtotal = db.Column(db.Float, default=0.0)  # Giá sau khi trừ chiết khấu
    product = db.relationship('AddProduct', backref='order_detail')
    order = db.relationship('Order', backref='order_detail', lazy=True)

    def __repr__(self):
        return f'<OrderDetail {self.id}: {self.product_name}>'