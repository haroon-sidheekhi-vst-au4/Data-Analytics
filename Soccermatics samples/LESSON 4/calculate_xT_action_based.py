# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 20:12:00 2022

@author: dev
"""
import pandas as pd
import json
# plotting
import os
import pathlib
import warnings
from joblib import load
from mplsoccer import Pitch
from itertools import combinations_with_replacement
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import numpy as np
pd.options.mode.chained_assignment = None
warnings.filterwarnings('ignore')

df = pd.DataFrame()
for i in range(11):
    file_name = 'possession_chains_England' + str(i+1) + '.json'
    with open('E:/SoccermaticsForPython-master/wyscout/possession_chain/'+str(file_name)) as d1:
        data = json.load(d1)
    df = pd.concat([df, pd.DataFrame(data)])
df = df.reset_index()

#model variables
var = ["x0", "x1", "c0", "c1"]

#combinations
inputs = []
#one variable combinations
inputs.extend(combinations_with_replacement(var, 1))
#2 variable combinations
inputs.extend(combinations_with_replacement(var, 2))
#3 variable combinations
inputs.extend(combinations_with_replacement(var, 3))

#make new columns
for i in inputs:
    #columns length 1 already exist
    if len(i) > 1:
        #column name
        column = ''
        x = 1
        for c in i:
            #add column name to be x0x1c0 for example
            column += c
            #multiply values in column
            x = x*df[c]
        #create a new column in df
        df[column] = x
        #add column to model variables
        var.append(column)
#investigate 3 columns
df[var[-3:]].head(3)

import pickle

#predict if ended with shot
passes = df.loc[df["eventName"].isin(["Pass"])]
X = passes[var].values
y = passes["shot_end"].values
#path to saved model
file = open('E:\Soccermatics\Soccermatics-main\course\lessons\possession_chain\finalized_model.sav')
model = pickle.load(file)
#predict probability of shot ended
y_pred_proba = model.predict_proba(X)[::,1]

passes["shot_prob"] = y_pred_proba
#OLS
shot_ended = passes.loc[passes["shot_end"] == 1]
X2 = shot_ended[var].values
y2 = shot_ended["xG"].values
lr = LinearRegression()
lr.fit(X2, y2)
y_pred = lr.predict(X)
passes["xG_pred"] = y_pred
#calculate xGchain
passes["xT"] = passes["xG_pred"]*passes["shot_prob"]

passes[["xG_pred", "shot_prob", "xT"]].head(5)


