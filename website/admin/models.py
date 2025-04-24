from website import db, app

class Admin(db.Model):
    __tablename__ = 'Admin'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(180), nullable=False, unique=False)
    profile = db.Column(db.String(180), nullable=False, unique=False, default='profile.jpg')

    def __repr__(self):
        return '<Admin %r>' % self.username
