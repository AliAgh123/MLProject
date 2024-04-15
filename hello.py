from flask import Flask
from flask import render_template
from flask import request
import joblib

app = Flask(__name__)

model = joblib.load('svc_model.pkl')


@app.route("/")
def hello_world():
    return render_template('hello.html')


@app.route('/submit', methods=['POST'])
def submit_form():
    data = [int(request.form.get('pregnancies')), int(request.form.get('glucose')), int(request.form.get('bloodPressure')), int(request.form.get('skinThickness')), int(request.form.get('insulin')), float(request.form.get('BMI')), float(request.form.get('diabetesPedigree')), int(request.form.get('age'))]

    prediction = model.predict([data])
    app.logger.debug(prediction)
    if(prediction == [0]):
        return render_template('healthy.html')
    elif (prediction == [1]):
        return render_template('diabetic.html')
    return "Error"