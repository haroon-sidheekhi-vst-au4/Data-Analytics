# -*- coding: utf-8 -*-
"""
Created on Thu Sep 16 16:45:39 2021

@author: dev
"""
#loading the DATA
import json


match_id = 3869685
with open('E:/SoccermaticsForPython-master/statsbomb02/open-data-master/data/events/'+str(match_id)+'.json',encoding="utf8") as d1:
    data = json.load(d1)

 
#making data more like an exel file
    from pandas import json_normalize
    df = json_normalize(data, sep = "_").assign(match_id = str(match_id)+'.json'[:-5])
    
    passes = df.loc[df['type_name'] == 'Pass'].set_index('id')
    salah = df.loc[df['player_name'] == 'Kylian Mbappé Lottin'].set_index('id')

#Drawing the pitch   
    from mplsoccer.pitch import Pitch
    pitch = Pitch(pitch_type='statsbomb', pitch_color='green', line_color='#c7d5cc' )
    fig, ax = pitch.draw()
    fig.set_facecolor('#22312b')

import matplotlib.pyplot as plt
pitchLengthX=120
pitchWidthY=80

#Looping to scatter the data
for i,passs in salah.iterrows():
    x=passs['location'][0]
    y=passs['location'][1]    
    
    circleSize=2
    pitch.scatter(x, pitchWidthY-y, ax=ax,s=100, edgecolor='black', facecolor='cornflowerblue')

plt.gca().invert_yaxis()        
ax.set_title('Touches by M.Salah against spurs in 2018-19 UEFA Final',fontsize = 14)
plt.show()
