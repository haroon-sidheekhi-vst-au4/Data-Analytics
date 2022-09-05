# -*- coding: utf-8 -*-
"""
Created on Tue Aug 30 15:54:37 2022

@author: dev
"""

#loading the DATA
import json
import pandas as pd
with open('E:\SoccermaticsForPython-master\statsbomb\data\competitions.json') as d1:
    competitions = json.load(d1)
    
    competition_id = 72
    season_id = 30
with open('E:/SoccermaticsForPython-master/statsbomb/data/matches/'+str(competition_id)+'/'+str(season_id)+'.json') as d2:
    matches = json.load(d2)
    
    match_id = 69301
with open('E:/SoccermaticsForPython-master/statsbomb/data/events/'+str(match_id)+'.json') as d3:
    data = json.load(d3)
from pandas import json_normalize
df = json_normalize(data, sep = "_").assign(match_id = str(match_id)+'.json'[:-5])
shots = df.loc[df['type_name'] == 'Shot'].set_index('id')
team1, team2 = df.team_name.unique()

shots["startX"] = shots["location"].apply(str).str.split(", ", expand=True)[0].str[1:].apply(pd.to_numeric)
shots["startY"] = shots["location"].apply(str).str.split(", ", expand=True)[1].str[:-1].apply(pd.to_numeric)
from mplsoccer.pitch import Pitch
import matplotlib.pyplot as plt
    
pitch = Pitch(line_color = "black",figsize=(10, 7))
fig, ax = pitch.draw()
#Size of the pitch in yards (!!!)
pitchLengthX = 120
pitchWidthY = 80
#Plot the shots by looping through them.
for i,shot in shots.iterrows():
    #get the information
    x=shot['startX']
    y=shot['startY']
    goal=shot['shot_outcome_name']=='Goal'
    team_name=shot['team_name']
    #set circlesize
    circleSize=2
    #plot England
    if (team_name==team1):
        if goal:
            shotCircle=plt.Circle((x,y),circleSize,color="red")
            plt.text(x+1,y-2,shot['player_name'])
        else:
            shotCircle=plt.Circle((x,y),circleSize,color="red")
            shotCircle.set_alpha(.2)
    #plot Sweden
    else:
        if goal:
            shotCircle=plt.Circle((pitchLengthX-x,pitchWidthY - y),circleSize,color="blue")
            plt.text(pitchLengthX-x+1,pitchWidthY - y - 2 ,shot['player_name'])
        else:
            shotCircle=plt.Circle((pitchLengthX-x,pitchWidthY - y),circleSize,color="blue")
            shotCircle.set_alpha(.2)
    ax.add_patch(shotCircle)
#set title
fig.suptitle("England (red) and Sweden (blue) shots", fontsize = 24)
fig.set_size_inches(10, 7)
plt.show()