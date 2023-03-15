import numpy as np
from flask import Flask, render_template, request, jsonify
import pickle




app = Flask(__name__)


#load the model
model = pickle.load(open('gradientboostmodel.pkl', 'rb'))
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
if __name__ ==  '__main__':
    app.run(debug=True)