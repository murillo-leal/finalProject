#models.py
from shelbyacai import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String, nullable=False)
    cellphone = db.Column(db.String, nullable=False)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    admin = db.Column(db.Boolean, nullable=True)

    orders = db.relationship('Order', backref='user', lazy=True)

    def __init__(self, email, password, username, address, cellphone):
        self.email = email
        self.address = address
        self.password_hash = generate_password_hash(password)
        self.username = username
        self.cellphone = cellphone

    def check_password(self, password):
        return  check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"Username{self.username}"          

class Order(db.Model):
    users = db.relationship(User)
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    products = db.relationship('Product', backref="productId", lazy='dynamic')    
    value = db.Column(db.String, nullable=False)
    payment = db.Column(db.String, nullable=False)

    def __init__(self,user_id, products, payment, value):
        payment = payment
        user_id = user_id
        products = products
        value = value

    def __repr__(self):
        return f"Order Id: {self.id} -- Date: {self.date} --- Products {self.products}"


class Toppings(db.Model):
    __tablename__ = 'toppings'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    value = db.Column(db.String, nullable=False)
    toppingType = db.Column(db.Integer, nullable=False)

    def __init__(self, name, value, toppingType):
        self.name = name
        self.value = value
        self.toppingType = toppingType

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    size = db.Column(db.String, nullable=False)
    value = db.Column(db.Integer, nullable=False)
    toppings = db.relationship(Toppings)

    def calculateFinalValue(self, toppings):
        return self.value + toppings.value

    def __init__(self, toppings, name, size, value, finalvalue):
        self.name = name
        self.toppings = toppings
        self.size = size
        self.value = value        
        self.finalvalue = finalvalue   

    def __repr__(self):
        return f"Product Id: {self.id} -- Product Size: {self.size} --- Product Value {self.value} ---  Product Toppings: {self.toppings}--- Toppings Value:{self.toppings.finalvalue}  --- Final Value:{self.finalvalue}"

