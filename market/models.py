from market import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(20), nullable=False, unique=True)
    email_address = db.Column(db.String(50), nullable=False, unique=True)

    password_hash = db.Column(db.String(255), nullable=False)

    budget = db.Column(db.Integer, nullable=False, default=500)
    total_spent = db.Column(db.Float, default=0)

    is_admin = db.Column(db.Boolean, default=False)

    items = db.relationship('Item', backref='owner_user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"User('{self.username}', '{self.email_address}')"


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(30), nullable=False, unique=True)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=False)

    owner = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"{self.name} - ${self.price}"
    
class MyCourse(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)

    user = db.relationship('User', backref='my_courses')
    item = db.relationship('Item')
 