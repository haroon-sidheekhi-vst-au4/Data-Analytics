# -*- coding: utf-8 -*-
"""
Created on Mon Sep  5 16:27:02 2022

@author: dev
"""

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
    team_name=pas['team_name']
    #set circlesize
    circleSize=1
    #plot England
    if (team_name=="Sweden Women's"):
        shotCircle=plt.Circle((x,y),circleSize,color="red")
        ax.add_patch(shotCircle)
        
#set title
ax.set_title("Starting point of every  "+ team2 + " passes", fontsize = 20)
fig.suptitle( "2019 FIFA WOMEN'S WORLD CUP", fontsize = 10)
fig.set_size_inches(10, 7)
plt.show()