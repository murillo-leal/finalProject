# orders/views.py

from flask import render_template,url_for, flash,request,redirect,Blueprint, session
from flask_login import current_user,login_required
from shelbyacai import db
from shelbyacai.models import Order, Product, Topping
from shelbyacai.orders.forms import OrderForm, ProductForm

order = Blueprint('order', __name__)
product = Blueprint('product', __name__)


#ORDER
@order.route('/order_cart', methods=['GET'])
@login_required
def order_cart():

    products_id_cart = session.get('cart', [])
    id2_count = len(products_id_cart)

    return render_template("order_cart.html", id=id2_count, products=products_id_cart)




#ADD PRODUCT
@order.route('/order/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if 'cart' not in session:
        session['cart'] = []

    
    form = ProductForm()
    form.toppings.choices = [(topping.value, topping.name)for topping in Topping]
    form.size.choices = [(product.id) for product in Product.query.all()]    

    if form.validate_on_submit():
        product_value =  form.toppings.data + form.size.data               
        product = Product(toppings=form.toppings.data,
                          size = form.size.data,
                          value=product_value
                          )
        session['cart'].append(product.id)
        flash('Product added')

        return redirect(url_for('order.order_cart'))       
    return render_template('product.html', form=form)

#Finish Order


#DELETE PRODUCT

#READ


#DELETE