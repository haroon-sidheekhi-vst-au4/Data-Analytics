# -*- coding: utf-8 -*-
"""
Created on Fri Sep 17 01:24:28 2021

@author: dev
"""

import json
match_id = 22912
with open('E:/SoccermaticsForPython-master/statsbomb/data/events/'+str(match_id)+'.json') as f:
    data = json.load(f)
    from pandas import json_normalize
    df = json_normalize(data, sep = "_").assign(match_id = str(match_id)+'.json'[:-5])
    
    Passes = df.loc[df['type_name'] == 'Pass'].set_index('id')
    
from mplsoccer.pitch import Pitch
    pitch = Pitch(pitch_type='statsbomb', pitch_color='w', line_color='#c7d5cc' ,figsize=(16, 11),constrained_layout=True, tight_layout=False )
    fig, ax = pitch.draw()
    fig.set_facecolor('#22312b')
    
    