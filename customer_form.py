from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Email
from wtforms.fields.html5 import EmailField


class createCustomer(FlaskForm):
    name = StringField("Customer Name: ", validators=[DataRequired()])
    phoneNumber = StringField("Phone Number: ", validators=[DataRequired()])
    email = EmailField("Email: ", validators=[InputRequired("Please Enter your Email address!!!")])
    address = StringField("Address: ", validators=[DataRequired()])
    city = StringField("City: ", validators=[DataRequired()])
    state = StringField("State: ", validators=[DataRequired()])
    submit = SubmitField("Submit")
