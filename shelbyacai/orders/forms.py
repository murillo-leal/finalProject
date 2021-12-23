# shelbyacai/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField, RadioField, SelectField
from wtforms.validators import DataRequired
from wtforms.widgets.core import Select


class ProductForm(FlaskForm):
    size = RadioField('Size',validators=[DataRequired()], choices=[])
    toppings = RadioField('Topppings',validators=[DataRequired()] ,choices=[])
    submit = SubmitField("Add Product")


class OrderForm(FlaskForm):
    payment = SelectField('Payment',validators=[DataRequired()], choices=[])    
    details = TextAreaField('Details',validators=[DataRequired()])
    submit = SubmitField("Finish Order")
