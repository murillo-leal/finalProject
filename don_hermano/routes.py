from flask import Flask, make_response, jsonify, g, render_template, flash, redirect, url_for, request, send_from_directory, session, abort

from flask_bcrypt import check_password_hash, generate_password_hash
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from flask_uploads import configure_uploads
from flask_wtf import file

from itsdangerous import URLSafeTimedSerializer

from threading import Thread

from werkzeug.datastructures import CombinedMultiDict, FileStorage
from werkzeug.utils import secure_filename
import os
import datetime
from . import forms
from . import models
import webbrowser

from peewee import SelectQuery

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecret'

app.config['UPLOADED_IMAGES_DEST'] = 'images/uploads/products'

configure_uploads(app, (forms.images,))

login_manager = LoginManager()

login_manager.init_app(app)
login_manager.login_view = 'user.login'


#UserRoutes
@app.route('/register', methods=('GET', 'POST'))
def register():
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        flash("Awesome! You have registered to our Site! ENJOY", category='Sucess')
        try:
            models.User.create_user(
                address=form.address.data,
                cellphone=form.cellphone.data,
                email=form.email.data,
                full_name=form.name.data,
                password=form.password.data
            )
            user = models.User.get(models.User.email == form.email.data)
            login_user(user)
        except ValueError:
            pass
        return redirect(url_for('index'))
    return render_template('register.html', form=form, user=current_user)


@app.route('/login/', methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash("Your email or password doesn't match", "Error")
        else:
            if check_password_hash(user.password.encode('utf-8'), form.password.data):
                login_user(user)
                if current_user.admin:
                    return redirect(url_for('index'))
                else:
                    flash("Successfully logged in!", "Success")
                    return redirect(url_for('index'))
            else:
                flash("Your email or password doesn't match", "Error")
    return render_template('login.html', form=form, user=current_user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Successfully logged out. Come back again!!", "Success")
    return redirect(url_for('index'))

@app.route('/profile/orders')
@login_required
def user_orders():
    products = models.Product.select(models.BuyHistory, models.Product).join(models.BuyHistory).annotate(models.BuyHistory, models.BuyHistory.product_quantity).where(models.BuyHistory.buyer == current_user.id)
    return render_template('user-orders.html', user=current_user, products=products)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():

    form = forms.UpdateUserForm()
    if form.validate_on_submit():
        user = models.User.get(models.User.email==current_user.email)
        print(form)
        current_user.address = form.address.data
        current_user.cellphone = form.cellphone.data
        current_user.email = form.email.data

        q = models.User.update(
            address=current_user.address,
            cellphone=current_user.cellphone,
            email=current_user.email,
            ).where(models.User.email==user.email)            
        q.execute()
        flash('User updated')
        redirect(url_for('index'))
    elif request.method=='GET':
        form.address.data=current_user.address
        form.email.data=current_user.email
        form.cellphone.data==current_user.cellphone
    return render_template('user-profile.html', user=current_user,form=form)


      




@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None

@app.before_request
def before_request():
    """Connet to the database before each request."""
    try:
        g.db = models.DATABASE
        g.db.connect()
    except models.OperationalError:
        pass


# @app.after_request
# def after_request(response):
#     """Close the database connection after each request."""
#     g.db.close()
#     return response

#INDEX
@app.route('/')
def index():    
    products=models.Product.select()
    return render_template("index.html", user=current_user, products=products)

@app.route('/about')
def about():
    return render_template("info.html", user=current_user)


#Products
@app.route('/products/burritos')
def products_burritos():
    products = models.Product.select().where(models.Product.category.contains('Burrito'))
    return render_template("products_burritos.html", user=current_user, products=products)    

@app.route('/products/nachos')
def products_nachos():
    products = models.Product.select().where(models.Product.category.contains('Nachos'))
    return render_template("products_nachos.html", user=current_user, products=products)

@app.route('/products/tacos')
def products_tacos():
    products = models.Product.select().where(models.Product.category.contains('Tacos'))
    return render_template("products_tacos.html", user=current_user, products=products)

@app.route('/products/quesadilla')
def products_quesadilla():
    products = models.Product.select().where(models.Product.category.contains('Quesadilla'))
    return render_template("products_quesadilla.html", user=current_user, products=products)       


#ProductRoute
@app.route('/products/<path:name>/', methods=['GET', 'POST'])
def product_index(name):
    try:
        product_ins = models.Product.get(models.Product.name == name)
    except models.Product.DoesNotExist:
        return abort(404)    
    return render_template("product/index.html", user=current_user, product=product_ins)
    
#AddProduct
@app.route('/buy_now/<int:product_id>/')
@login_required
def buy_now(product_id):
    try:
        if models.Order.get((models.Order.user_email == current_user.id) & (models.Order.product_id == product_id)):
            print('1')
            prod = models.Order.get((models.Order.user_email == current_user.id) & (models.Order.product_id == product_id))
            q = models.Order.update(count = prod.count + 1).where((models.Order.user_email == current_user.id) & (models.Order.product_id == product_id))
            q.execute()
    except models.Order.DoesNotExist:
        print('2')
        models.Order.add_product(
            user_email=current_user.id,
            product_id_id=product_id,
            count = 1
        )            
    return redirect(url_for('checkout'))  

#DELETE PRODUCT
@app.route('/delete_order/<int:product_id>/', methods=('GET', 'POST'))
@login_required
def delete_order(product_id):
    try:
        prod = models.Order.get((models.Order.user_email == current_user.id) & (models.Order.product_id == product_id))
        prod.delete_instance()
    except models.Order.DoesNotExist:
        pass
    return redirect(url_for('order_index'))      

#READ
@app.route('/add_order/<int:product_id>', methods=('GET', 'POST'))
@login_required
def add_order(product_id):
    try:
        if models.Order.get((models.Order.user_email == current_user.id) & (models.Order.product_id == product_id)):
            print('1')
            prod = models.Order.get((models.Order.user_email == current_user.id) & (models.Order.product_id == product_id))
            q = models.Order.update(count = prod.count + 1).where((models.Order.user_email == current_user.id) & (models.Order.product_id == product_id))
            q.execute()
    except models.Order.DoesNotExist:
        print('2')
        models.Order.add_product(
            user_email=current_user.id,
            product_id_id=product_id,
            count=1
        )
    flash("Successfully added to cart!")
    return redirect(url_for('order_index'))

#Order
@app.route('/order/',methods=('GET', 'POST'))
@login_required
def order_index():
    products = models.Product.select(models.Order, models.Product).join(models.Order).annotate(models.Order, models.Order.count).where(models.Order.user_email == current_user.id)
    return render_template('order.html', user=current_user, products=products)

@app.route('/checkout/', methods=('GET', 'POST'))
@login_required
def checkout():
    products = {}
    order_details = "Hello, I'm {}%0aThat's My Order:%0a".format(current_user.full_name)
    totalprice = 0
    try:
        products = models.Product.select(models.Order, models.Product).join(models.Order).annotate(models.Order, models.Order.count).where(models.Order.user_email == current_user.id)
        for prod in products:
            totalprice += prod.value * prod.order.count
            order_details+="%0a"+prod.category+" "+prod.name+" value: "+str(prod.value)+" quantity: "+str(prod.order.count)

        order_details += "%0aTotal value: " + str(totalprice) + "%0a"

    except models.Order.DoesNotExist:
        pass

    if request.method == 'POST':
        name = request.form['fullname']
        address = request.form['address']
        cellphone = request.form['cellphone']
        payment_option = request.form['payment']
        
        for product in products:
            models.BuyHistory.add_history(
                buyer = current_user.id,
                product_id=product.id,
                product_name=product.name,
                product_quantity=product.order.count,
                buyer_name=name,
                buyer_address=address,
                mobile_no=cellphone,
                payment_option=payment_option
            )

        order_details += "%0aAddress: {}".format(address)
        order_details += "%0aPayment Option: {}".format(payment_option)

        try:
            ins= models.Order.delete().where(models.Order.user_email==current_user.id)
            ins.execute()
        except models.Order.DoesNotExist:
            pass
        flash("You Order has been placed Successfully!", "Success")
        webbrowser.open_new_tab("https://wa.me/+5512991479029/?text={}".format(order_details))
        redirect(url_for('index'))
    return render_template("checkout.html", user=current_user, products=products, totalprice=totalprice, orderdetails=order_details)                   
        
#Search route
@app.route("/search", methods=['POST', 'GET'])
def search():
    query = request.args.get('keyword')
    print(query)
    products = models.Product.select().where(models.Product.name.regexp(query.replace(' ', '|')))
    return render_template('search.html', user=current_user, products=products, query=query)


@app.route('/product_images')
def uploaded_file():
    filename = request.args.get('image')
    return send_from_directory(os.path.join(app.instance_path, app.config['UPLOADED_IMAGES_DEST']), filename)

#Admin route
@app.route('/dashboard/products/new', methods=['GET', 'POST'])
@login_required
def dashboard_product_new():
    if current_user.admin:
        form=forms.NewProductForm(CombinedMultiDict((request.files, request.form)))
        filename = ''
        if form.validate_on_submit():
            if form.image.data:
                f= form.image.data
                filename= secure_filename(f.filename)
                f.save(os.path.join(
                    app.instance_path, app.config['UPLOADED_IMAGES_DEST'], filename
                ))
            models.Product.add_product(
                name=form.name.data,
                image=filename,
                size=form.size.data,
                count=form.count.data,
                value=form.value.data,
                category=form.category.data,
                details=form.details.data,
            )
            return redirect(url_for('dashboard_product_new'))
        return render_template("dashboard/product/new.html", user=current_user, form=form)
    else:
        return redirect(url_for('index'))

@app.route('/dashboard/products/edit/<id>', methods=('GET', 'POST'))
@login_required
def dashboard_product_edit(id):
    if current_user.admin:
        product = models.Product.get(models.Product.id == id)
        form = forms.EditProductForm(CombinedMultiDict((request.files, request.form)), obj=product)
        filename = ''

        if form.validate_on_submit():
            if(form.image.data):
                f = form.image.data
                if type(f)==FileStorage:
                    filename=secure_filename(f.filename)
                    f.save(os.path.join(
                        app.instance_path, app.config['UPLOADED_IMAGES_DEST'], filename
                    ))
                else:
                    filename=f
            q = models.Product.update(
            name=form.name.data,
            image=filename,
            size=form.size.data,
            count=form.count.data,
            value=form.value.data,
            category=form.category.data,
            details=form.details.data,
            ).where(models.Product.id==id)
            q.execute()
        return render_template('dashboard/product/edit.html', user=current_user,form=form, item=product)
    else:
        return redirect(url_for('index'))

@app.route('/dashboard/products/delete/<id>', methods=('GET', 'POST'))
@login_required
def dashboard_product_delete(id):
    if current_user.admin:
        product_ins = models.Product.get(models.Product.id == id)
        product_ins.delete_instance()
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))       

@app.route('/dashboard/orders/')
@login_required
def dashboard_orders():
    if current_user.admin:
        return render_template("dashboard/orders.html", user=current_user, products=models.BuyHistory, app=app)
    else:
        return redirect(url_for('index'))