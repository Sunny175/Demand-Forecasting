import pickle
import numpy as np
from flask import Flask, render_template, request, url_for, redirect, flash
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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


db.create_all()


@app.route('/')
def home():
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
    return render_template("dashboard.html", name=current_user.name)

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
    return redirect(url_for("home"))


@app.route('/secrets')
@login_required
def secrets():
    return render_template("secrets.html", name=current_user.name)


if __name__ == '__main__':
    app.run(debug=True)
