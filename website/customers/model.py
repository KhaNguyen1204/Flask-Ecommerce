from website import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def user_loader(user_id):
    return Register.query.get(int(user_id))

class Register(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=False)
    username = db.Column(db.String(50), unique=False, nullable=False)
    email = db.Column(db.String(100), unique=False, nullable=False)
    password = db.Column(db.String(100), unique=False, nullable=False)
    country = db.Column(db.String(50), unique=False, nullable=False)
    city = db.Column(db.String(50), unique=False, nullable=False)
    contact = db.Column(db.String(50), unique=False, nullable=False)
    address = db.Column(db.String(200), unique=False, nullable=False)
    zipcode = db.Column(db.String(50), unique=False, nullable=False)
    profile = db.Column(db.String(200), unique=False, default='profile.png')
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return '<User %r>' % self.name

    # Flask-Login required properties
    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)