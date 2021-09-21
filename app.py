#!/usr/bin/python
# -*- coding:Utf-8 -*-

################################################################################
#               Importations des bibliothèques
################################################################################

import statsmodels.api as sm
import pandas as pd
import urllib.request
from joblib import load
from flask import Flask, render_template, request
from bs4 import BeautifulSoup


################################################################################
#               Définition des fonctions
################################################################################

# Conversion conso : l/100kg -> mpg
def conv_conso(val):
    return (100 * 3.785411784) / (val * 1.609344)

# Conversion longueur : cm -> inch
def conv_long(val):
    return val * 0.393701

# Conversion poid : kg -> lbs
def conv_poid(val):
    return val * 2.20462

# Conversion prix : $ -> €
def conv_prix(val):
    header = "'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'"
    url = 'https://www.google.fr/search?q=usd+euro'
    request = urllib.request.Request(url)
    request.add_header('User-Agent', header)
    response = urllib.request.urlopen(request).read()
    html = response.decode("utf-8")
    soup = BeautifulSoup(html, 'html.parser')
    taux = soup.select_one("span.DFlfde.SwHCTb").attrs.get("data-value", None)
    return round(val*float(taux), 2)

# Prédiction du prix par rapport au modèle
def prediction(X):
    model = load('model.joblib')
    return round(model.predict(X)[0], 2)


################################################################################
#               Interface Flask
################################################################################

app = Flask(__name__)

@app.route('/')
def home():
    title = 'Paramètre du véhicule à estimer'
    return render_template('form.html', title=title)

@app.route('/estim', methods=['post'])
def estim():
    title = 'Estimation du prix'
    price = {}
    sys = request.form.get('system', type=str)
    data = pd.DataFrame()
    data['cylindernumber'] = [request.form.get('cylindernumber', type=int)]
    data['carlength'] = [request.form.get('carlength', type=float)]
    data['carwidth'] = [request.form.get('carwidth', type=float)]
    data['curbweight'] = [request.form.get('curbweight', type=int)]
    data['compressionratio'] = [request.form.get('compressionratio', type=float)]
    data['horsepower'] = [request.form.get('horsepower', type=int)]
    data['highwaympg'] = [request.form.get('highwaympg', type=float)]
    price['price'] = prediction(data)
    price['unit'] = '$'
    if sys == 'metric':
        data['carlength'] = conv_long(data['carlength'])
        data['carwidth'] = conv_long(data['carwidth'])
        data['curbweight'] = conv_poid(data['curbweight'])
        data['highwaympg'] = conv_conso(data['highwaympg'])
        price['price'] = prediction(data)
        price['price'] = conv_prix(price['price'])
        price['unit'] = '€'
    return render_template('result.html', title=title, price=price, sys=sys)

if __name__ == '__main__':
    app.run()
