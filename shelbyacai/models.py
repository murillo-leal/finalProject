#models.py
from sqlalchemy.orm import backref, relation, relationship
from shelbyacai import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
import enum

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String, nullable=False)
    cellphone = db.Column(db.String, nullable=False)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    admin = db.Column(db.Boolean, nullable=True)
    order = db.relationship("Order", backref= "order", lazy='dynamic') 


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

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class Topping(enum.Enum):
    OREO  = 4
    MILK = 1
    GRANOLA = 1
    BANANA = 1
    NESCAUBALL = 2
    PAÇOCA = 3

product_order = db.Table('product_order',
    db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True))

class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.String, nullable=False)
    value = db.Column(db.Integer, nullable=False)    
    toppings = db.Column(db.Enum(Topping))

    def calculateFinalValue(self):
        return self.value + self.toppings.value

    def __init__(self, toppings, size, value):
        self.toppings = toppings
        self.size = size
        self.value = value        

    def __repr__(self):
        return f"Product Id: {self.id} -- Product Size: {self.size} --- Product Value {self.value} ---  Product Toppings: {self.toppings}--- Toppings Value:{self.toppings.finalvalue}  --- Final Value:{self.finalvalue}"

class Order(db.Model):
    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    value = db.Column(db.String, nullable=False)
    payment = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    details = db.Column(db.Text)
    product = db.relationship('Product', secondary=product_order, lazy='subquery')    

    def __init__(self,user_id, products, payment, value, details):
        payment = payment
        user_id = user_id
        products = products
        value = value
        details = details

    def __repr__(self):
        return f"Order Id: {self.id} -- Date: {self.date} --- Products {self.products}"       




