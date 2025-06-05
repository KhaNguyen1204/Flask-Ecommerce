from shop import db
from datetime import datetime

# Warehouse model
class Warehouse(db.Model):
    __tablename__ = 'warehouses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    capacity = db.Column(db.Integer, nullable=True)
    description = db.Column(db.Text, nullable=True)
    manager_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(db.String(20), default='active')  # Active, Inactive

    # Relationships
    manager = db.relationship('Staff', backref='managed_warehouses', foreign_keys=[manager_id])
    inbound_receipts = db.relationship('InboundReceipt', backref='warehouse', lazy=True)
    outbound_receipts = db.relationship('OutboundReceipt', backref='warehouse', lazy=True)

    def __repr__(self):
        return f'<Warehouse {self.name}>'

# Inbound Receipt (phiếu nhập)
class InboundReceipt(db.Model):
    __tablename__ = 'inbound_receipts'
    id = db.Column(db.Integer, primary_key=True)
    receipt_number = db.Column(db.String(50), nullable=False, unique=True)
    receipt_date = db.Column(db.DateTime, default=datetime.now)
    supplier = db.Column(db.String(100), nullable=True)
    total_amount = db.Column(db.Float, default=0)
    notes = db.Column(db.Text, nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.id'), nullable=False)
    status = db.Column(db.String(20), default='Đang xử lý')  # Đang xử lý, Đã hoàn thành, Đã hủy

    # Relationships
    creator = db.relationship('Staff', backref='created_inbound_receipts', foreign_keys=[created_by])
    receipt_details = db.relationship('InboundReceiptDetail', backref='receipt', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<InboundReceipt {self.receipt_number}>'

# Inbound Receipt Details (chi tiết phiếu nhập)
class InboundReceiptDetail(db.Model):
    __tablename__ = 'inbound_receipt_details'
    id = db.Column(db.Integer, primary_key=True)
    inbound_receipt_id = db.Column(db.Integer, db.ForeignKey('inbound_receipts.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, default=0)
    notes = db.Column(db.Text, nullable=True)

    # Relationships
    product = db.relationship('AddProduct', backref='inbound_details')

    def __repr__(self):
        return f'<InboundReceiptDetail {self.id}>'

# Outbound Receipt (phiếu xuất)
class OutboundReceipt(db.Model):
    __tablename__ = 'outbound_receipts'
    id = db.Column(db.Integer, primary_key=True)
    receipt_number = db.Column(db.String(50), nullable=False, unique=True)
    receipt_date = db.Column(db.DateTime, default=datetime.now)
    recipient = db.Column(db.String(100), nullable=True)
    total_amount = db.Column(db.Float, default=0)
    notes = db.Column(db.Text, nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.id'), nullable=False)
    status = db.Column(db.String(20), default='Đang xử lý')  # Đang xử lý, Đã hoàn thành, Đã hủy

    # Relationships
    creator = db.relationship('Staff', backref='created_outbound_receipts', foreign_keys=[created_by])
    receipt_details = db.relationship('OutboundReceiptDetail', backref='receipt', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<OutboundReceipt {self.receipt_number}>'

# Outbound Receipt Details (chi tiết phiếu xuất)
class OutboundReceiptDetail(db.Model):
    __tablename__ = 'outbound_receipt_details'
    id = db.Column(db.Integer, primary_key=True)
    outbound_receipt_id = db.Column(db.Integer, db.ForeignKey('outbound_receipts.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, default=0)
    notes = db.Column(db.Text, nullable=True)

    # Relationships
    product = db.relationship('AddProduct', backref='outbound_details')

    def __repr__(self):
        return f'<OutboundReceiptDetail {self.id}>'
