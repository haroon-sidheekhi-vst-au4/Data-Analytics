# -*- coding: utf-8 -*-
"""
Created on Mon Sep  5 16:36:34 2022

@author: dev
"""

#
#loading the DATA
import json
import pandas as pd 
match_id = 69301
with open('E:/SoccermaticsForPython-master/statsbomb/data/events/'+str(match_id)+'.json') as d1:
    data = json.load(d1)
from pandas import json_normalize
df = json_normalize(data, sep = "_").assign(match_id = str(match_id)+'.json'[:-5])
Passes = df.loc[df['type_name'] == 'Pass'].set_index('id')
team1, team2 = df.team_name.unique()

Passes["startX"] = Passes["location"].apply(str).str.split(", ", expand=True)[0].str[1:].apply(pd.to_numeric)
Passes["startY"] = Passes["location"].apply(str).str.split(", ", expand=True)[1].str[:-1].apply(pd.to_numeric)
Passes["endX"] = Passes["pass_end_location"].apply(str).str.split(", ", expand=True)[0].str[1:].apply(pd.to_numeric)
Passes["endY"] = Passes["pass_end_location"].apply(str).str.split(", ", expand=True)[1].str[:-1].apply(pd.to_numeric)

from mplsoccer.pitch import Pitch
import matplotlib.pyplot as plt
    
pitch = Pitch(line_color = "black",figsize=(10, 7))
fig, ax = pitch.draw()
#Size of the pitch in yards (!!!)
pitchLengthX = 120
pitchWidthY = 80
#Plot the shots by looping through them.
for i,pas in Passes.iterrows():
    #get the information
    x=pas['startX']
    y=pas['startY']
    xx=pas['endX']-x
    yy=pas['endY']-y
    team_name=pas['team_name']
    player_name=pas['player_name']
    #set circlesize
    circleSize=0.5
    #plot England
    if (player_name=="Sara Caroline Seger"):
        shotCircle=plt.Circle((x,y),circleSize,color="red")
        passArrow=plt.Arrow(x,y,xx,yy,width=2,color="red")
        ax.add_patch(shotCircle)
        ax.add_patch(passArrow)
#set title
ax.set_title("Caroline Seger Passes vs "+ team1, fontsize = 20)
fig.suptitle( "2019 FIFA WOMEN'S WORLD CUP", fontsize = 10)
fig.set_size_inches(10, 7)
plt.show()