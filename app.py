#!/usr/bin/python
# -*- coding:Utf-8 -*-

################################################################################
#               Importations des bibliothèques
################################################################################

import statsmodels.api as sm
import pandas as pd
from joblib import load
from flask import Flask, render_template, request


################################################################################
#               Définition des fonctions
################################################################################

def conv_conso(val):
    return (100 * 3.785411784) / (val * 1.609344)


def estimate(X):
    model = load('model.joblib')
    return round(model.predict(X)[0], 2)


################################################################################
#               Interface Flask
################################################################################

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('form.html', title="Paramètre du véhicule à estimer")

@app.route('/estimate', methods=['post'])
def estim():
    data = pd.DataFrame()
    data['cylindernumber'] = [request.form.get('cylindernumber', type=int)]
    data['carlength'] = [request.form.get('carlength', type=float)]
    data['carwidth'] = [request.form.get('carwidth', type=float)]
    data['curbweight'] = [request.form.get('curbweight', type=int)]
    data['compressionratio'] = [request.form.get('compressionratio', type=float)]
    data['horsepower'] = [request.form.get('horsepower', type=int)]
    data['highwaympg'] = [request.form.get('highwaympg', type=int)]
    print(data)
    estimate_price = estimate(data)
    return render_template('result.html', title="Estimation du prix", price=estimate_price, data=data)

if __name__ == '__main__':
    app.run(debug=True)
