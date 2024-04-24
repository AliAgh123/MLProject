from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
import xgboost as xgb
import joblib

app = Flask(__name__)

model = joblib.load('xgb_model.pkl')

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/predict")
def predict():
    return render_template('form.html', outOfRange=False, isNumerical = False)

@app.route('/submit', methods=['POST'])
def submit_form():
    pregnancies = request.form.get('pregnancies') if request.form.get('pregnancies') != 0 else 4 # 0 --> 17
    glucose = request.form.get('glucose') if request.form.get('glucose') != 0 else 123 # 44 --> 200
    bloodPressure = request.form.get('bloodPressure') if request.form.get('bloodPressure') != 0 else 73 # 24 --> 122
    skinThickness = request.form.get('skinThickness') if request.form.get('skinThickness') != 0 else 30 # 7 --> 100
    insulin = request.form.get('insulin') if request.form.get('insulin') != 0 else 155 # 14 --> 846
    BMI = float(request.form.get('BMI')) if request.form.get('BMI') != 0 else 32.39 # 18.20 --> 67.10
    # diabetesPedigree = float(request.form.get('diabetesPedigree'))
    age = request.form.get('age') if request.form.get('age') != 0 else 33 # not negative
    data = [[int(pregnancies), int(glucose), int(bloodPressure), int(skinThickness), int(insulin), BMI, int(age)]] # without diabetes pedigree
    
    if(isinstance(BMI, float)):
        return render_template('form.html', outOfRange = False, isNumerical = True)
    
    if (data[0][0] < 0 or data[0][0] > 17 or data[1][0] < 44 or data[1][0] > 200 or data[2][0] < 24 or data[2][0] > 122 or data[3][0] < 7 or data[3][0] > 100 or data[4][0] < 14 or data[4][0] > 846 or data[5][0] < 18.20
        or data[5][0] > 67.10 or data[6][0] < 0):
        return render_template('form.html', outOfRange = True, isNumerical = False)
    
    app.logger.debug(data)
    prediction = model.predict(xgb.DMatrix(data))
    app.logger.debug(prediction)
    if(prediction < [0.5]):
        return render_template('healthy.html')
    elif (prediction >= [0.5]):
        return render_template('diabetic.html')
    return "Error"