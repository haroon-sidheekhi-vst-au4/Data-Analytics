# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 22:47:46 2022

@author: dev
"""

# -*- coding: utf-8 -*-

"""
with open('E:\SoccermaticsForPython-master\statsbomb\data\competitions.json') as f:
    competitions = json.load(f)
with open('E:/SoccermaticsForPython-master/statsbomb/data/matches/16/4.json') as f:
    matches = json.load(f)"""

#Function to draw the pitch
import matplotlib.pyplot as plt
import numpy as np

#Size of the pitch in yards (!!!)
pitchLengthX=120
pitchWidthY=80

#ID   
match_id_required = 22912
home_team_required ="Liverpool"
away_team_required ="Tottenham Hotspur"

file_name=str(match_id_required)+'.json'

#Load in all match events 
import json
with open('E:/SoccermaticsForPython-master/statsbomb/data/events/'+file_name) as data_file:
    #print (mypath+'events/'+file)
    data = json.load(data_file)

#get the nested structure into a dataframe 
#store the dataframe in a dictionary with the match id as key (remove '.json' from string)
from pandas.io.json import json_normalize
from pandas.io import json
df = json_normalize(data, sep = "_").assign(match_id = file_name[:-5])

#A dataframe of Passes
passes = df.loc[df['type_name'] == 'Pass'].set_index('id')

#Drawing the pitch
from mplsoccer.pitch import Pitch
pitch = Pitch(pitch_type='statsbomb', pitch_color='w', line_color='#c7d5cc' ,figsize=(16, 11),constrained_layout=True, tight_layout=False )
fig, ax = pitch.draw()
fig.set_facecolor('#22312b')


#plotiing
for i,pas in passes.iterrows(): #Mohamed Salah Roberto Firmino Barbosa de Oliveira Sadio ManÃ©
    if pas['player_name']=="Mohamed Salah": # if pas['possession_team_name']=="Liverpool":
        x=pas['location'][0]
        y=pas['location'][1]
        xx=pas['pass_end_location'][0]
        yy=pas['pass_end_location'][1]
        circleSize=1
        passInit=plt.Circle((x,y),circleSize,color="red")
        passInit.set_alpha(0.2)
        ax.add_patch(passInit)
        pitch.arrows(x, y,xx, yy, width=2,headwidth=10, headlength=10, color='#ad993c', ax=ax, label='completed passes')
        ax=ax
        passText=plt.text(5,75,'Passes made by '+ pas['player_name'] + ' Liverpool attackers in 2019 UCL final', fontsize=18) 
        ax.add_patch(passInit)
