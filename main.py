from flask import Flask, render_template, request
import pickle



app = Flask(__name__)


#load the model
model = pickle.load(open('gradientboostmodel.pkl', 'rb'))
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST', 'GET'])
def predict():
    category = model.predict(request.form("category"))
    cuisine = model.predict(request.form("cuisine"))
    week = model.predict(request.form("week"))
    check_out = model.predict(request.form("checkout_price"))
    base_price = model.predict(request.form("base_price"))
    emailer = model.predict(request.form("emailer"))
    homepage = model.predict(request.form("homepage"))
    city = model.predict(request.form("city"))
    region = model.predict(request.form("region"))
    op_area = model.predict(request.form("op_area"))
    center_type = model.predict(request.form("center_type"))
    print(model.predict(category, cuisine, week, check_out, base_price, emailer, homepage, city, region, op_area, center_type))

    return render_template('index.html')

if __name__ ==  '__main__':
    app.run(debug=True)