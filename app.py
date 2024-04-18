from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
import joblib

app = Flask(__name__)

model = joblib.load('svc_model.pkl')

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/predict")
def predict():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    pregnancies = request.form.get('pregnancies')
    glucose = request.form.get('glucose')
    bloodPressure = request.form.get('bloodPressure')
    skinThickness = request.form.get('skinThickness')
    insulin = request.form.get('insulin')
    BMI = float(request.form.get('BMI'))
    diabetesPedigree = float(request.form.get('diabetesPedigree'))
    age = request.form.get('age')
    data = [pregnancies, glucose, bloodPressure, skinThickness, insulin, BMI, diabetesPedigree, age]
    prediction = model.predict([data])
    app.logger.debug(prediction)
    if(prediction == [0]):
        return render_template('healthy.html')
    elif (prediction == [1]):
        return render_template('diabetic.html')
    return "Error"