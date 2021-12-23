# shelbyacai/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_migrate import Migrate
from flask_login import LoginManager, login_manager

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecret'

## Database Setup###

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
Migrate(app, db)

############################
## Login Configs

login_manager = LoginManager()

login_manager.init_app(app)
login_manager.login_view = 'user.login'


###########################


from shelbyacai.core.views import core
from shelbyacai.error_pages.handlers import error_pages
from shelbyacai.users.views import users
from shelbyacai.orders.views import order, product

app.register_blueprint(users)
app.register_blueprint(core)
app.register_blueprint(error_pages)
app.register_blueprint(order)
app.register_blueprint(product)
