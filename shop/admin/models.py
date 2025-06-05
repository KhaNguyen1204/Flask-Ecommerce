from shop import db, app
from datetime import datetime
from shop.models import User

class Staff(User):
    __tablename__ = 'staff'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    salary = db.Column(db.Float, default=0)
    position = db.Column(db.String(50), nullable=False, unique=False)
    hire_date = db.Column(db.DateTime, default=datetime.now)

    __mapper_args__ = {'polymorphic_identity': 'staff'}

    def __repr__(self):
        return '<Staff %r>' % self.username

