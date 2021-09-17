#!/usr/bin/python
# -*- coding:Utf-8 -*-

################################################################################
#               Importations des bibliothèques
################################################################################

import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn import datasets, linear_model
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from joblib import dump


################################################################################
#               Importation des données
################################################################################

PATH = 'Ressources/RAW/cars.csv'

df = pd.read_csv(PATH)


################################################################################
#               Nettoyage des données
################################################################################

# Marques
df[['marque','modele']] = df['CarName'].str.split(' ', n=1, expand=True)
df['marque'] = df['marque'].replace('alfa-romero', 'alfa-romeo')
df['marque'] = df['marque'].replace('Nissan', 'nissan')
df['marque'] = df['marque'].replace('porcshce', 'porsche')
df['marque'] = df['marque'].replace('Nissan', 'nissan')
df['marque'] = df['marque'].replace('maxda', 'mazda')
df['marque'] = df['marque'].replace('vokswagen', 'volkswagen')
df['marque'] = df['marque'].replace('vw', 'volkswagen')
df['marque'] = df['marque'].replace('toyouta', 'toyota')
df['marque'] = df['marque'].astype('str')

# Nombre de portes
df['doornumber'] = df['doornumber'].replace('two', '2')
df['doornumber'] = df['doornumber'].replace('four', '4')
df['doornumber'] = df['doornumber'].astype('int')

# Nombre de cylindres
df['cylindernumber'] = df['cylindernumber'].replace('two', '2')
df['cylindernumber'] = df['cylindernumber'].replace('three', '3')
df['cylindernumber'] = df['cylindernumber'].replace('four', '4')
df['cylindernumber'] = df['cylindernumber'].replace('five', '5')
df['cylindernumber'] = df['cylindernumber'].replace('six', '6')
df['cylindernumber'] = df['cylindernumber'].replace('eight', '8')
df['cylindernumber'] = df['cylindernumber'].replace('twelve', '12')
df['cylindernumber'] = df['cylindernumber'].astype('int')


################################################################################
#               Selection des données pour le modèle
################################################################################

Y = df['price']

X = df[['cylindernumber',
'carlength',
'carwidth',
'curbweight',
'compressionratio',
'horsepower',
'highwaympg']]


################################################################################
#               Entrainement du modèle
################################################################################

# Entrainement StatsModels
# model = sm.OLS(Y, X, missing='drop').fit()
# dump(model, 'model.joblib')

# Entrainement SkLearn
model = linear_model.LinearRegression().fit(X, Y)
dump(model, 'model.joblib')
