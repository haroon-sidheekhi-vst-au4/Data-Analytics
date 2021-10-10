# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 15:29:05 2021

@author: dev
"""

match_id_required = 69301
home_team_required ="England Women's"
away_team_required ="Sweden Women's"

file_name=str(match_id_required)+'.json'

#Load in all match events 
import json
with open('E:/SoccermaticsForPython-master/statsbomb/data/events/'+file_name) as data_file:
    data = json.load(data_file)
    
from pandas import json_normalize
df = json_normalize(data, sep = "_").assign(match_id = file_name[:-5])
shots = df.loc[df['type_name'] == 'Shot'].set_index('id')

#Drawing the pitch
from mplsoccer.pitch import Pitch
pitch = Pitch(pitch_type='statsbomb', pitch_color='w', line_color='#c7d5cc' ,figsize=(16, 11),constrained_layout=True, tight_layout=False )
fig, ax = pitch.draw()
fig.set_facecolor('#22312b')


#plotiing
import matplotlib.pyplot as plt
import numpy as np
pitchLengthX=120
pitchWidthY=80
for i,shot in shots.iterrows():
    x=shot['location'][0]
    y=shot['location'][1]
    
    goal=shot['shot_outcome_name']=='Goal'
    team_name=shot['team_name']
    plt.gca().invert_yaxis()
    #circleSize=2
    circleSize=np.sqrt(shot['shot_statsbomb_xg'])*12

    if (team_name==home_team_required):
        if goal:
            shotCircle=plt.Circle((x,pitchWidthY-y),circleSize,color="red")
            plt.text((x+1),pitchWidthY-y+1,shot['player_name'].split()[0]) 
        else:
            shotCircle=plt.Circle((x,pitchWidthY-y),circleSize,color="red")     
            shotCircle.set_alpha(.2)
            #plt.text((x+1),pitchWidthY-y+1,shot['player_name'].split()[0])
    elif (team_name==away_team_required):
        if goal:
            shotCircle=plt.Circle((pitchLengthX-x,y),circleSize,color="blue") 
            plt.text((pitchLengthX-x+1),y+1,shot['player_name'].split()[0]) 
        else:
            shotCircle=plt.Circle((pitchLengthX-x,y),circleSize,color="blue")      
            shotCircle.set_alpha(.2)
            #plt.text((pitchLengthX-x+1),y+1,shot['player_name'].split()[0]) 
    ax.add_patch(shotCircle)
    
    
plt.text(5,75,away_team_required + ' shots') 
plt.text(80,75,home_team_required + ' shots') 
fig.set_size_inches(10, 7)
