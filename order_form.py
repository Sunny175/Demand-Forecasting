from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired


class OrderForm(FlaskForm):
    product = StringField("Product Name", validators=[DataRequired()])
    status = SelectField("Status", choices=["out for delivery", "pending", "Delivered"])
    submit = SubmitField("Submit")
