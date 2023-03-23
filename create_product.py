from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField
from wtforms.validators import DataRequired


class createProduct(FlaskForm):
    name = StringField("Name: ", validators=[DataRequired()])
    cuisine = StringField("Cuisine: ", validators=[DataRequired()])
    price = StringField("Price: ", validators=[DataRequired()])
    submit = SubmitField("Submit")
