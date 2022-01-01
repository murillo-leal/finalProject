#models.py
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from peewee import *
from playhouse.migrate import SqliteMigrator
import uuid


##Database
DATABASE = SqliteDatabase('don_hermano.db')
migrator = SqliteMigrator(DATABASE)

class User(UserMixin, Model):
    """User Table"""
    full_name = CharField()
    address = CharField()
    cellphone = CharField()
    email = CharField(unique=True)
    password = CharField()
    admin = BooleanField(default=False)

    class Meta:
        database=DATABASE
            
    @classmethod
    def create_user(cls, full_name, address, cellphone, email, password, admin=False):
        try:
            cls.create(
                full_name=full_name,
                email=email,
                password = generate_password_hash(password),
                cellphone=cellphone,
                address=address,
                admin=admin
            )
        except IntegrityError:
            raise ValueError("User already exists")

    # def check_password(self, password):
    #     return  check_password_hash(self.password_hash, password)

    # def __repr__(self):
    #     return f"Username{self.username}"     


class Product(Model):
    "Products Table"
    name = CharField()
    image = CharField()
    size = CharField()
    count = IntegerField()
    value = IntegerField(null=False)
    category = CharField()   
    details = CharField()
    published_at = DateTimeField(default=datetime.now)


    class Meta:
        database = DATABASE
        order_by = ('-published_at',)

    @classmethod
    def add_product(cls, name, size, image, value, category, details,count):
        try:            
            cls.create(
                name=name,
                size=size,
                count=count,
                image=image,
                value=value,
                category=category,
                details=details
            )
        except:
            raise ValueError("Some Error Happened")


class Order(Model):
    user_email = ForeignKeyField(User, related_name='orders')
    product_id = ForeignKeyField(Product, related_name='products')
    count = IntegerField()  

    class Meta:
        database = DATABASE

    @classmethod
    def add_product(cls, user_email, product_id_id, count=1):
        try:
            cls.create(
                user_email=user_email,
                product_id_id=product_id_id,
                count=count
            )
        except:
            raise ValueError("Some error happened!")      

    


class BuyHistory(Model):
    """Item Buying History"""
    order_id = CharField(max_length=50, unique=True)
    product_id = ForeignKeyField(Product, related_name='product')
    buyer = ForeignKeyField(User, related_name='customer')
    product_name = CharField()       
    buyer_name = CharField()       
    mobile_no = CharField()
    payment_option = CharField()
    product_quantity = IntegerField()
    buyer_address = CharField()
    buy_time = DateTimeField(null = True, default = datetime.now)

    class Meta:
        database = DATABASE
        order_by = ('buy_time',)

    @classmethod
    def add_history(cls, buyer, product_id, product_name, buyer_name, mobile_no, payment_option, product_quantity, buyer_address):
        cls.create(
            order_id=str(uuid.uuid4()),
            buyer=buyer,
            product_id=product_id,
            product_name=product_name,
            buyer_name=buyer_name,
            mobile_no=mobile_no,
            payment_option=payment_option,
            product_quantity=product_quantity,
            buyer_address=buyer_address
        )


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Product, BuyHistory, Order], safe=True)
    DATABASE.close()
