import pickle
import numpy as np
from flask import Flask, render_template, request, url_for, redirect, flash
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bootstrap import Bootstrap
from customer_form import createCustomer
from create_product import createProduct
from order_form import OrderForm
import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Bootstrap(app)

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
# load the model
model = pickle.load(open('gradientboostmodel.pkl', 'rb'))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(1000))
    name = db.Column(db.String(1000))


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    address = db.Column(db.String(100))
    phoneNumber = db.Column(db.Integer, unique=True)
    city = db.Column(db.String(20))
    state = db.Column(db.String(20))
    mail = db.Column(db.String)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    cuisine = db.Column(db.String(20))
    price = db.Column(db.Integer)


class order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer)
    date_created = db.Column(db.String)
    status = db.Column(db.String)
    product = db.Column(db.String)


db.create_all()


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST', 'GET'])
def predict():
    model = pickle.load(open('gradientboostmodel.pkl', 'rb'))
    category = request.form['category']
    cuisine = int(request.form['cuisine'])
    week = int(request.form['week'])
    checkout_price = float(request.form['checkout_price'])
    base_price = float(request.form['base_price'])
    emailer = int(request.form['emailer'])
    homepage = int(request.form['homepage'])
    city = int(request.form['city'])
    region = int(request.form['region'])
    op_area = float(request.form['op_area'])
    center_type = int(request.form['center_type'])
    category = int(category)
    list = [category, cuisine, week, checkout_price, base_price, emailer, homepage, city, region, op_area,
            center_type]
    data = np.asarray([list])
    output = model.predict(data)
    output = int(output)
    print(output)
    if output < 0:
        output = 0
    return render_template("index.html", output=output, week=week)


@app.route("/sales")
def sales():
    return render_template("sales.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if not user:
            flash("That email does not exist, please try again.")
        elif not check_password_hash(user.password, password):
            flash("Password incorrect, please try again.")
            return redirect(url_for("login"))
        else:
            login_user(user)
            return redirect(url_for("dashboard", name=user.name))
    return render_template("login.html")


@app.route("/dashboard")
@login_required
def dashboard():
    totalCustomer = db.session.query(Customer.id).count()
    all_customers = Customer.query.all()
    all_orders = order.query.all()
    total_orders = db.session.query(order.id).count()
    status = db.session.query(order.status, func.count(order.status).label("out for delivery")).group_by(
        order.status).all()
    cancel = status[0][1]
    out_for_delivery = status[1][1]
    delivered = status[2][1]
    pending = status[3][1]

    return render_template("dashboard.html", name=current_user.name, totalCustomer=totalCustomer,
                           all_customers=all_customers, all_orders=all_orders, total_orders=total_orders, cancel=cancel,
                           out_for_delivery=out_for_delivery, delivered=delivered, pending=pending)


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        if User.query.filter_by(email=request.form.get("email")).first():
            flash("You have already signedup with that email, log in instead.")
            return redirect(url_for("login"))
        hash_and_salted_password = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256',
                                                          salt_length=8
                                                          )
        new_user = User(
            email=request.form.get('email'),
            name=request.form.get('name'),
            password=hash_and_salted_password,
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("login"))
    return render_template('register.html')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route('/create-customer', methods=["GET", "POST"])
def create_customer():
    form = createCustomer()
    if form.validate_on_submit():
        new_customer = Customer(
            name=form.name.data,
            phoneNumber=form.phoneNumber.data,
            address=form.address.data,
            city=form.city.data,
            state=form.state.data
        )
        db.session.add(new_customer)
        db.session.commit()
        return redirect(url_for('dashboard', name=current_user.name))
    return render_template("create_customer.html", form=form)


@app.route('/create-product', methods=["GET", "POST"])
def create_product():
    form = createProduct()
    if form.validate_on_submit():
        new_product = Product(
            name=form.name.data,
            cuisine=form.cuisine.data,
            price=form.price.data
        )
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('dashboard', name=current_user.name))
    return render_template("create_product.html", form=form)


@app.route('/customer-details/<id>')
def customer_details(id):
    customer = Customer.query.get(id)
    total_items = db.session.query(order.customer_id, func.count(order.customer_id)).group_by(order.customer_id)
    total_products = db.session.query(order).filter(order.customer_id == int(id))
    for item in total_items:
        if int(id) == item[0]:
            total_orders = item
            return render_template("customer_details.html", name=current_user.name, customer=customer, total_orders=total_orders, total_products=total_products)
    return render_template("customer_details.html", name=current_user.name, customer=customer)


@app.route("/place-order/<id>")
def place_new_order(id):
    form = OrderForm()
    if form.validate_on_submit():
        new_order = order(
            customer_id=id,
            date_created=str(datetime.date.today()),
            status=form.status.data,
            product=form.product.data
        )
        db.session.add(new_order)
        db.session.commit()
        return render_template("place_new_order.html")
    return render_template("place_new_order.html", name=current_user.name, form=form)

if __name__ == '__main__':
    app.run(debug=True)
