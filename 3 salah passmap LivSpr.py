# -*- coding: utf-8 -*-
"""
Created on Fri Sep 17 01:24:28 2021

@author: dev
"""

import json
match_id = 7581
with open('E:/SoccermaticsForPython-master/statsbomb/data/events/'+str(match_id)+'.json') as f:
    data = json.load(f)
    from pandas import json_normalize
    df = json_normalize(data, sep = "_").assign(match_id = str(match_id)+'.json'[:-5])
    
    Passes = df.loc[df['type_name'] == 'Pass'].set_index('id')
    
    from mplsoccer.pitch import Pitch
    pitch = Pitch(pitch_type='statsbomb', pitch_color='#22312b', line_color='#c7d5cc',figsize=(16, 11), constrained_layout=True, tight_layout=False)
    fig, ax = pitch.draw()
    fig.set_facecolor('#22312b')
            

for i,pas in Passes.iterrows():
    x=pas['location'][0]
    y=pas['location'][1]
    endx = pas['pass_end_location'][0]
    endy = pas['pass_end_location'][1]
    name=pas['player_name']=='Virgil van Dijk'
    if name:
        pitch.scatter(x, y, ax=ax,s=100, edgecolor='black', facecolor='cornflowerblue')
        pitch.arrows(x,y,endx,endy, width=2,headwidth=10, headlength=10, color='#ad993c', ax=ax, label='completed passes')
    
ax.set_title('VVD vs Spurs', color='#dee6ea',fontsize=25)
