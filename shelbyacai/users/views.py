# users/views.py
from flask import render_template, url_for, flash,request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import redirect
from shelbyacai import db
from shelbyacai.models import User, Order
from shelbyacai.users.forms import RegistrationForm, LoginForm, UpdateUserForm

users = Blueprint('users', __name__)

#register




#login

#logout
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("core.index"))

#account(update UserForm)
#user's list of orders